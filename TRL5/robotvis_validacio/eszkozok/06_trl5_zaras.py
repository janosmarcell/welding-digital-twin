#!/usr/bin/env python3
"""TRL 5 záró kiértékelés: a T5-01, a T5-08 és a kezelői próba kapuja egy riportban.

Bemenetek (a jóváhagyási lap aláírása után):
  - T5-01: az automata kulcs és a vakon kitöltött annotációs lap (CSV, UTF-8);
  - T5-08: egy vagy több `T5-08_visszajatszas_futasok.csv` (05_visszajatszas_kiertekelo.py kimenete),
           valamint a cellás videók összesítése (T5-08_video_osszesites.md);
  - kezelői próba: a kitöltött ellenőrzőlista (kezeloi_ellenorzolista_sablon.csv alapján).

Kimenet: <out>/TRL5_ZARO_RIPORT.md és <out>/trl5_zaras.json. Kilépési kód: 0, ha mindhárom kapu teljesül.

A kapuk értékei a jóváhagyási lapról jönnek; a --t501-feltetel kötelező, hogy a döntés ne utólag szülessen.
"""
import argparse, csv, json, math, os, re, sys, hashlib, datetime


def wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def num(x):
    try:
        s = str(x).strip().replace(",", ".")
        return None if s == "" or s.lower() == "nan" else float(s)
    except ValueError:
        return None


# ---------------------------------------------------------------- T5-01
def t501(kulcs, kitoltott, tol, feltetel, kapu_pont, kapu_also, tajek=()):
    key = {r["azonosito"]: r for r in read_csv(kulcs)}
    ann_all = read_csv(kitoltott)
    is_t = lambda a: any(a.startswith(p + "_") for p in tajek)
    ann = [r for r in ann_all if not is_t(r["azonosito"])]
    tajek_sorok = []
    for r in ann_all:
        if is_t(r["azonosito"]):
            k = key.get(r["azonosito"], {})
            tajek_sorok.append((r["azonosito"], r.get("kezdet_sor", ""), k.get("auto_kezdet_sor", ""), r.get("veg_sor", ""), k.get("auto_veg_sor", ""), (r.get("megjegyzes") or "").strip()))
    n_ev = n_ok = 0
    kivetelek, annotator = [], set()
    for r in ann:
        if (r.get("annotator") or "").strip():
            annotator.add(r["annotator"].strip())
        k = key.get(r["azonosito"], {})
        for nev, ak, uk in (("kezdet", "kezdet_sor", "auto_kezdet_sor"), ("vég", "veg_sor", "auto_veg_sor")):
            x, y = num(r.get(ak)), num(k.get(uk))
            if x is None:
                kivetelek.append((r["azonosito"], nev, "nincs annotáció", (r.get("megjegyzes") or "").strip()))
                continue
            n_ev += 1
            if y is None:
                kivetelek.append((r["azonosito"], nev, "nincs automatikus szakasz", (r.get("megjegyzes") or "").strip()))
                continue
            d = int(x) - int(y)
            if abs(d) <= tol:
                n_ok += 1
            else:
                kivetelek.append((r["azonosito"], nev, f"eltérés {d:+d} sor", (r.get("megjegyzes") or "").strip()))
    arany = n_ok / n_ev if n_ev else float("nan")
    lo, hi = wilson(n_ok, n_ev)
    ok = bool(n_ev) and (arany >= kapu_pont if feltetel == "pont" else lo >= kapu_also)
    felt = f"pontbecslés ≥ {kapu_pont:.0%}" if feltetel == "pont" else f"Wilson 95% alsó határ ≥ {kapu_also:.0%}"
    nem_annotalt = sum(1 for x in kivetelek if x[2] == "nincs annotáció")
    return dict(varrat=len(ann), esemeny=n_ev, nem_annotalt=nem_annotalt, tajekoztato=tajek_sorok, tajekoztato_naplok=list(tajek), egyezo=n_ok, arany=arany, wilson_also=lo, wilson_felso=hi,
                tures_sor=tol, feltetel=felt, teljesul=ok, kivetelek=kivetelek, annotator=sorted(annotator),
                fajlok={os.path.basename(kulcs): sha256(kulcs), os.path.basename(kitoltott): sha256(kitoltott)})


# ---------------------------------------------------------------- T5-08
def t508(futas_csvk, video_md, cel_ms, min_futas):
    futasok = []
    for p in futas_csvk:
        for r in read_csv(p):
            futasok.append(dict(forras=os.path.basename(os.path.dirname(os.path.abspath(p))), futas=r["futas"],
                                pozicio_P95_ms=num(r["pozicio_P95_ms"]), aramforras_P95_ms=num(r["aramforras_P95_ms"]),
                                megallas_db=int(num(r["megallas_db"]) or 0),
                                aramforras_kimaradt=int(num(r.get("aramforras_kimaradt")) or 0),
                                aramforras_kuldve=int(num(r.get("aramforras_kuldve")) or 0)))
    rossz = [f for f in futasok if f["pozicio_P95_ms"] is None or f["pozicio_P95_ms"] > cel_ms
             or (f["aramforras_P95_ms"] is not None and f["aramforras_P95_ms"] > cel_ms)]
    video = []
    if video_md and os.path.exists(video_md):
        for line in open(video_md, encoding="utf-8"):
            if line.startswith("|") and ".csv" in line:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                m = re.search(r"([0-9]+,[0-9]+|[0-9]+(?:\.[0-9]+)?)\s*s\b", cells[-1])
                if m:
                    fb = float(m.group(1).replace(",", "."))
                elif re.match(r"kb\. 0\b", cells[-1]):
                    fb = 0.0  # egy képkockán belül
                else:
                    fb = None  # nem mérhető
                video.append(dict(futas=cells[0], felso_becsles_s=fb,
                                  megjegyzes=cells[-1]))
    vmert = [v["felso_becsles_s"] for v in video if v["felso_becsles_s"] is not None]
    video_ok = all(v * 1000 <= cel_ms for v in vmert)
    ok = len(futasok) >= min_futas and not rossz and video_ok
    return dict(futasok=futasok, futas_db=len(futasok), rossz=rossz, video_db=len(video), video_mert_db=len(vmert),
                video_max_s=max(vmert) if vmert else None, video_ok=video_ok, cel_ms=cel_ms, min_futas=min_futas,
                teljesul=ok)


# ---------------------------------------------------------------- kezelői próba
def kezeloi(lista, min_ertheto):
    rows = {str(r["pont"]).strip(): r for r in read_csv(lista)}
    ig = lambda p: (rows.get(p, {}).get("valasz") or "").strip().lower() in ("igen", "i", "yes", "1")
    hianyzo = [p for p in ("1", "2", "3", "4") if not ig(p)]
    e = num(rows.get("7", {}).get("valasz"))
    ok = not hianyzo and e is not None and e >= min_ertheto
    return dict(pontok={p: (rows[p].get("valasz") or "").strip() for p in sorted(rows, key=lambda s: int(s) if s.isdigit() else 99)},
                megjegyzesek={p: (rows[p].get("megjegyzes") or "").strip() for p in rows if (rows[p].get("megjegyzes") or "").strip()},
                nem_teljesult_pontok=hianyzo, ertheto=e, min_ertheto=min_ertheto, teljesul=ok,
                fajl={os.path.basename(lista): sha256(lista)})


def fmt_ms(x):
    return "–" if x is None else f"{x:.0f} ms"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--t501-kulcs", required=True)
    ap.add_argument("--t501-kitoltott", required=True)
    ap.add_argument("--t501-feltetel", required=True, choices=["pont", "wilson"],
                    help="a jóváhagyási lapon választott feltétel: (a) pont = pontbecslés, (b) wilson = CI alsó határ")
    ap.add_argument("--t501-kapu-pont", type=float, default=0.99)
    ap.add_argument("--t501-kapu-also", type=float, default=0.95)
    ap.add_argument("--tol-sor", type=int, default=1)
    ap.add_argument("--t501-tajekoztato", default="g02_s33", help="vesszővel elválasztott naplók, amelyek külön, a kapun kívül szerepelnek (alapértelmezés: g02_s33, ismert naplókiesés)")
    ap.add_argument("--t508-futasok", nargs="+", required=True, help="T5-08_visszajatszas_futasok.csv fájl(ok)")
    ap.add_argument("--t508-video", default=None, help="T5-08_video_osszesites.md")
    ap.add_argument("--t508-cel-ms", type=float, default=2000)
    ap.add_argument("--t508-min-futas", type=int, default=3)
    ap.add_argument("--kezeloi-lista", required=True, help="a kitöltött kezelői ellenőrzőlista (CSV)")
    ap.add_argument("--kezeloi-min-ertheto", type=float, default=3)
    ap.add_argument("--szimulalt", action="store_true", help="próbafuttatás nem valós bemenettel: a riport fejléce jelöli")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    tajek = tuple(x.strip() for x in a.t501_tajekoztato.split(",") if x.strip())
    r1 = t501(a.t501_kulcs, a.t501_kitoltott, a.tol_sor, a.t501_feltetel, a.t501_kapu_pont, a.t501_kapu_also, tajek)
    r8 = t508(a.t508_futasok, a.t508_video, a.t508_cel_ms, a.t508_min_futas)
    rk = kezeloi(a.kezeloi_lista, a.kezeloi_min_ertheto)
    mind = r1["teljesul"] and r8["teljesul"] and rk["teljesul"]
    V = lambda b: "**TELJESÜL**" if b else "**NEM TELJESÜL**"
    most = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    L = ["# TRL 5 – záró kiértékelés", ""]
    if a.szimulalt:
        L += ["> **SZIMULÁLT PRÓBAFUTTATÁS – nem mérési eredmény, nem bizonyíték.**", ""]
    L += [f"Készült: {most}; eszköz: `06_trl5_zaras.py`. A kapuk a jóváhagyási lap szerint.", "",
          "| Kapu | Feltétel | Eredmény | Döntés |", "| --- | --- | --- | --- |",
          f"| T5-01 | {r1['feltetel']}, ±{r1['tures_sor']} sor | {r1['egyezo']}/{r1['esemeny']} = {r1['arany']:.1%}; Wilson 95%: {r1['wilson_also']:.3f}–{r1['wilson_felso']:.3f} | {V(r1['teljesul'])} |",
          f"| T5-08 | P95 ≤ {a.t508_cel_ms/1000:g} s minden futásban, ≥ {a.t508_min_futas} futás | {r8['futas_db']} visszajátszott futás; videó: {r8['video_mert_db']} mért futás, max. ≤ {r8['video_max_s'] if r8['video_max_s'] is not None else '–'} s | {V(r8['teljesul'])} |",
          f"| Kezelői próba | 1–4. pont „igen”, 7. pont ≥ {a.kezeloi_min_ertheto:g} | 7. pont: {rk['ertheto'] if rk['ertheto'] is not None else '–'}; nem teljesült: {', '.join(rk['nem_teljesult_pontok']) or 'nincs'} | {V(rk['teljesul'])} |",
          "", f"**Összesen: {'a TRL 5 zárókapui teljesülnek' if mind else 'a TRL 5 zárókapui NEM teljesülnek'}.**"
          + (" A lezáráshoz még kell: a jegyzőkönyv kitöltése és aláírása (végrehajtó, kezelő, minőségügyi szakértő)." if mind else ""), ""]

    L += ["## T5-01 – eseményfelismerés", "",
          f"- Annotált varrat: {r1['varrat']}; kiértékelt esemény: {r1['esemeny']}; egyező: {r1['egyezo']}",
          f"- Nem annotált (üresen hagyott) esemény: {r1['nem_annotalt']}",
          f"- Annotátor: {', '.join(r1['annotator']) or '(nincs megadva)'}", f"- Kivételek: {len(r1['kivetelek'])}", ""]
    if r1["kivetelek"]:
        L += ["| Azonosító | Esemény | Ok | Az annotátor megjegyzése |", "| --- | --- | --- | --- |"]
        L += [f"| {x[0]} | {x[1]} | {x[2]} | {x[3]} |" for x in r1["kivetelek"]]
        L += [""]

    if r1["tajekoztato"]:
        L += [f"### Tájékoztató, a kapun kívül: {', '.join(r1['tajekoztato_naplok'])}", "",
              "Ismert naplókiesés (2,5 s, az 1. és 2. varrat közötti szünetben): az automata az 1. és 2. varratot egy szakasznak látja, ezért a sorszám szerinti párosítás itt nem értelmezhető. Az annotáció és a kulcs összevetése:", "",
              "| Azonosító | Annotált kezdet | Automata kezdet | Annotált vég | Automata vég | Megjegyzés |", "| --- | --- | --- | --- | --- | --- |"]
        L += [f"| {x[0]} | {x[1]} | {x[2]} | {x[3]} | {x[4]} | {x[5]} |" for x in r1["tajekoztato"]]
        L += [""]
    L += ["## T5-08 – streaming késleltetés", "", "| Forrás | Futás | Pozíció P95 | Áramforrás-érték P95 | Megállás | Áramforrás-érték kimaradt |",
          "| --- | --- | --- | --- | --- | --- |"]
    L += [f"| {f['forras']} | {f['futas']} | {fmt_ms(f['pozicio_P95_ms'])} | {fmt_ms(f['aramforras_P95_ms'])} | {f['megallas_db']} | {f['aramforras_kimaradt']}/{f['aramforras_kuldve']} |" for f in r8["futasok"]]
    L += ["", f"Cellás videók: {r8['video_db']} futás, ebből {r8['video_mert_db']} mérhető; a késés felső becslése legfeljebb {r8['video_max_s']} s.",
          "Az áramforrás-értékek kimaradása dokumentált korlát (nem kapu); a javítás a TRL 6 előtt kerül be.", ""]

    L += ["## Kezelői próba", "", "| Pont | Válasz | Megjegyzés |", "| --- | --- | --- |"]
    L += [f"| {p} | {v} | {rk['megjegyzesek'].get(p, '')} |" for p, v in rk["pontok"].items()]
    L += ["", "## Bemenetek (SHA-256)", ""]
    for d in (r1["fajlok"], rk["fajl"]):
        L += [f"- `{k}`: `{v}`" for k, v in d.items()]
    L += [f"- `{p}`: `{sha256(p)}`" for p in a.t508_futasok]
    if a.t508_video:
        L += [f"- `{a.t508_video}`: `{sha256(a.t508_video)}`"]

    open(os.path.join(a.out, "TRL5_ZARO_RIPORT.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    js = dict(szimulalt=a.szimulalt, keszult=most, mind_teljesul=mind, t501={k: v for k, v in r1.items()},
              t508=r8, kezeloi=rk)
    json.dump(js, open(os.path.join(a.out, "trl5_zaras.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("\n".join(L[:12]))
    sys.exit(0 if mind else 1)


if __name__ == "__main__":
    main()
