#!/usr/bin/env python3
"""
05_visszajatszas_kiertekelo.py - a visszajátszásos T5-08 mérés kiértékelése.

Bemenet:
  --kuldes   a 04_visszajatszo.py kuldesi_naplo.csv fájlja
  --robotvis a RobotVis által a futások alatt írt CSV-k (a "user://" naplómappából; a fájlnév a futás
             prefixével kezdődik, pl. futas1_2026-11-05_10-12-3.csv)
Kimenet (--out mappa): T5-08_visszajatszas_futasok.csv, T5-08_visszajatszas_esemenyek.csv, T5-08_visszajatszas_riport.md

Mérőszámok futásonként:
  - pozíció: a küldéstől a RobotVis-napló első olyan soráig tartó idő (3 s-os ablakon belül), amelyben az adott pozíció szerepel
    (a RobotVis képkockánként naplóz, ezért az egy képkockán belül érkezett pozíciók közül csak az utolsó
    kerül a naplóba: ezt "összevont"-ként számoljuk, nem adatvesztésként);
  - áramforrás-érték (TorchSignal, feszültség, áram): a küldéstől (a teszt-oldal frissítésétől) a napló első
    egyező soráig tartó idő; ha a következő érték előbb megjelenik, az érték "kimaradt" (a Selenium-olvasás
    ciklusa miatt);
  - megállás: két egymást követő naplósor között 2 s-nál nagyobb idő.
Mindkét időbélyeg ugyanannak a PC-nek a rendszerórájából származik.
"""
import argparse, csv, glob, os, re
import statistics as st


def pct(v, p):
    v = sorted(v)
    if not v:
        return float("nan")
    k = (len(v) - 1) * p / 100.0
    lo, hi = int(k), min(int(k) + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def key_pos(vals):
    return tuple(round(float(x), 3) for x in vals)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kuldes", required=True)
    ap.add_argument("--robotvis", nargs="+", required=True)
    ap.add_argument("--out", default="T5-08_visszajatszas")
    ap.add_argument("--cel-ms", type=float, default=2000)
    ap.add_argument("--megallas-ms", type=float, default=2000)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    sent = {}
    with open(a.kuldes, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            sent.setdefault(r["futas"], []).append(r)

    files = []
    for p in a.robotvis:
        files += glob.glob(p)
    summary, events = [], []
    for run in sorted(sent):
        cand = [p for p in files if os.path.basename(p).startswith(run + "_")]
        if not cand:
            print(f"{run}: nincs RobotVis-napló (a fájlnévnek '{run}_' előtaggal kell kezdődnie)")
            continue
        with open(sorted(cand)[-1], encoding="utf-8-sig") as f:
            log = list(csv.DictReader(f))
        lt = [int(r["SysTimeMsecs"]) for r in log]
        # pozíciók: első megjelenés a naplóban
        pos_times = {}
        for r, t in zip(log, lt):
            k = key_pos([r[c] for c in ("X", "Y", "Z", "Rx", "Ry", "Rz")])
            pos_times.setdefault(k, []).append(t)

        def first_after(k, ts, win=3000):
            for t in pos_times.get(k, []):
                if ts - 5 <= t <= ts + win:
                    return t
            return None
        pos_lat, pos_coalesced = [], 0
        powr = []
        for s in sent[run]:
            ts = float(s["t_kuldes_ms"])
            if s["fajta"] == "pozicio":
                k = key_pos([s[c] for c in "abcdef"])
                t = first_after(k, ts)
                if t is None:
                    pos_coalesced += 1
                else:
                    pos_lat.append(t - ts)
                    events.append(dict(futas=run, fajta="pozicio", forras_sor=s["forras_sor"], kesleltetes_ms=round(t - ts, 1)))
            else:
                powr.append(s)
        # áramforrás-értékek: a napló első egyező sora a küldés után, a következő érték küldése előtt
        pow_lat, pow_missed, torch_lat = [], 0, []
        j = 0
        for n, s in enumerate(powr):
            ts = float(s["t_kuldes_ms"])
            t_next = float(powr[n + 1]["t_kuldes_ms"]) if n + 1 < len(powr) else float("inf")
            want = (int(s["a"]), round(float(s["b"]), 2), round(float(s["c"]), 1))
            while j < len(lt) and lt[j] < ts - 5:
                j += 1
            hit = None
            for m in range(j, len(lt)):
                if lt[m] > t_next + 3000:
                    break
                r = log[m]
                got = (int(float(r["TorchSignal"])), round(float(r["Voltage"]), 2), round(float(r["Current"]), 1))
                if got == want:
                    hit = lt[m]
                    break
            if hit is None or hit > t_next + 3000:
                pow_missed += 1
                continue
            pow_lat.append(hit - ts)
            is_torch = n > 0 and int(powr[n - 1]["a"]) != int(s["a"])
            if is_torch:
                torch_lat.append(hit - ts)
            events.append(dict(futas=run, fajta="torch" if is_torch else "aramforras", forras_sor=s["forras_sor"], kesleltetes_ms=round(hit - ts, 1)))
        gaps = [b - a_ for a_, b in zip(lt, lt[1:])]
        stalls = sum(1 for g in gaps if g > a.megallas_ms)
        row = dict(futas=run, naplo=os.path.basename(sorted(cand)[-1]), naplo_sorok=len(log),
                   pozicio_kuldve=len(pos_lat) + pos_coalesced, pozicio_naplozva=len(pos_lat), pozicio_osszevont=pos_coalesced,
                   pozicio_P50_ms=round(pct(pos_lat, 50), 1), pozicio_P95_ms=round(pct(pos_lat, 95), 1), pozicio_max_ms=round(max(pos_lat or [float("nan")]), 1),
                   aramforras_kuldve=len(powr), aramforras_kimaradt=pow_missed,
                   aramforras_P50_ms=round(pct(pow_lat, 50), 1), aramforras_P95_ms=round(pct(pow_lat, 95), 1), aramforras_max_ms=round(max(pow_lat or [float("nan")]), 1),
                   torch_valtas_db=len(torch_lat), torch_max_ms=round(max(torch_lat or [float("nan")]), 1),
                   leghosszabb_naplores_ms=max(gaps or [0]), megallas_db=stalls)
        summary.append(row)

    with open(os.path.join(a.out, "T5-08_visszajatszas_futasok.csv"), "w", newline="", encoding="utf-8") as f:
        if summary:
            w = csv.DictWriter(f, fieldnames=list(summary[0].keys())); w.writeheader(); w.writerows(summary)
    with open(os.path.join(a.out, "T5-08_visszajatszas_esemenyek.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["futas", "fajta", "forras_sor", "kesleltetes_ms"]); w.writeheader(); w.writerows(events)

    ok = len(summary) >= 3 and all(r["pozicio_P95_ms"] <= a.cel_ms and r["aramforras_P95_ms"] <= a.cel_ms for r in summary)
    L = ["# T5-08 – visszajátszásos mérés (valós cellás CSV-k, valós RobotVis, robot és áramforrás nélkül)", "",
         f"- Futások: {len(summary)} (követelmény: ≥ 3); cél: P95 ≤ {a.cel_ms:.0f} ms a pozícióra és az áramforrás-értékekre minden futásban (jóváhagyandó).",
         "- A mérés a forrás (visszajátszó) és a RobotVis-napló között méri a késést; a kijelzés ugyanabban a képkockában frissül, mint a naplózás.",
         "- Nem méri: a valós robotvezérlő és áramforrás belső késését (ezt a cellás videók becslik), a hálózati kapcsolat hibáit a cellában.", "",
         "| Futás | Pozíció P50 / P95 / max [ms] | Összevont pozíció | Áramforrás P50 / P95 / max [ms] | Kimaradt érték | TorchSignal-váltás max [ms] | Leghosszabb naplórés [ms] | Megállás > 2 s |",
         "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in summary:
        L.append(f"| {r['futas']} | {r['pozicio_P50_ms']} / {r['pozicio_P95_ms']} / {r['pozicio_max_ms']} | {r['pozicio_osszevont']} / {r['pozicio_kuldve']} | "
                 f"{r['aramforras_P50_ms']} / {r['aramforras_P95_ms']} / {r['aramforras_max_ms']} | {r['aramforras_kimaradt']} / {r['aramforras_kuldve']} | "
                 f"{r['torch_max_ms']} ({r['torch_valtas_db']} db) | {r['leghosszabb_naplores_ms']} | {r['megallas_db']} |")
    L += ["", f"**{'A KÉSLELTETÉSI FELTÉTEL TELJESÜL' if ok else 'A KÉSLELTETÉSI FELTÉTEL NEM TELJESÜL VAGY NINCS ELÉG FUTÁS'}** "
          "(a kimaradt értékeket és a megállásokat a jegyzőkönyvben külön kell értékelni)."]
    open(os.path.join(a.out, "T5-08_visszajatszas_riport.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
