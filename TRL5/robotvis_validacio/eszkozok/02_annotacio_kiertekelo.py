#!/usr/bin/env python3
"""T5-01 kiértékelő: kézi annotáció és az automatikus szakaszhatárok (TorchSignal) összevetése.

Használat:
  python3 -I 02_annotacio_kiertekelo.py --kulcs automata_kulcs.csv --kitoltott annotacio_sablon.csv --out <mappa> [--tol-sor 1] [--kapu 0.99]
Egy esemény megfelel, ha |annotált sor - automatikus sor| <= tol-sor (1 sor = 1 rögzített mintavételi periódus).
"""
import argparse, math, os
import pandas as pd


def wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kulcs", required=True); ap.add_argument("--kitoltott", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--tol-sor", type=int, default=1); ap.add_argument("--kapu", type=float, default=0.99)
    ap.add_argument("--tajekoztato", default="g02_s33", help="vesszővel elválasztott naplók, amelyek külön, a kapun kívül szerepelnek")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    key = pd.read_csv(a.kulcs, encoding="utf-8-sig"); ann = pd.read_csv(a.kitoltott, encoding="utf-8-sig")
    tajek = [x.strip() for x in a.tajekoztato.split(",") if x.strip()]
    is_t = ann["azonosito"].astype(str).apply(lambda v: any(v.startswith(p + "_") for p in tajek))
    ann_t = ann[is_t].merge(key, on="azonosito", how="left"); ann = ann[~is_t]
    if len(ann_t):
        ann_t.to_csv(os.path.join(a.out, "T5-01_tajekoztato.csv"), index=False, encoding="utf-8-sig")
    m = ann.merge(key, on="azonosito", how="left")
    rows, ev_total, ev_ok = [], 0, 0
    for _, r in m.iterrows():
        res = dict(azonosito=r["azonosito"], annotalt_kezdet=r["kezdet_sor"], auto_kezdet=r["auto_kezdet_sor"], annotalt_veg=r["veg_sor"], auto_veg=r["auto_veg_sor"],
                   auto_szakaszok_szama=r["auto_szakaszok_szama"], megjegyzes=r.get("megjegyzes", ""))
        for nev, ak, uk in (("kezdet", "kezdet_sor", "auto_kezdet_sor"), ("veg", "veg_sor", "auto_veg_sor")):
            x, y = r[ak], r[uk]
            if pd.isna(x) or str(x).strip() == "":
                res[nev + "_eredmeny"] = "nincs annotáció"; continue
            ev_total += 1
            if pd.isna(y) or str(y).strip() == "":
                res[nev + "_eredmeny"] = "nincs automatikus szakasz"; continue
            diff = int(float(x)) - int(float(y)); res[nev + "_elteres_sor"] = diff
            if abs(diff) <= a.tol_sor:
                ev_ok += 1; res[nev + "_eredmeny"] = "egyezik"
            else:
                res[nev + "_eredmeny"] = "ELTÉR"
        rows.append(res)
    out = pd.DataFrame(rows); out.to_csv(os.path.join(a.out, "T5-01_eredmeny.csv"), index=False, encoding="utf-8-sig")
    ratio = ev_ok / ev_total if ev_total else float("nan"); lo, hi = wilson(ev_ok, ev_total)
    kiv = out[(out.get("kezdet_eredmeny") != "egyezik") | (out.get("veg_eredmeny") != "egyezik")]
    verdict = "A KAPU TELJESÜL" if ev_total and ratio >= a.kapu else "A KAPU NEM TELJESÜL"
    md = [f"# T5-01 eredmény", "",
          f"- Annotált varrat (a kapuban): {len(ann)}; kiértékelt esemény: {ev_total}; egyező: {ev_ok}; arány: {ratio:.3f}",
          f"- Tájékoztató, a kapun kívül: {', '.join(tajek) or '-'} ({len(ann_t)} varrat, T5-01_tajekoztato.csv)",
          f"- Wilson 95% CI: {lo:.3f} – {hi:.3f}",
          f"- Tűrés: ±{a.tol_sor} sor; javasolt kapu: ≥ {a.kapu:.2f} (jóváhagyandó)",
          f"- **{verdict}** (a pontbecslés alapján; a CI alsó határa: {lo:.3f})",
          "", f"Kivételek (listázandók a jegyzőkönyvben): {len(kiv)}", ""]
    if len(kiv):
        md.append(kiv.to_markdown(index=False) if hasattr(kiv, "to_markdown") else kiv.to_string(index=False))
    md += ["", "Megjegyzés: kis esemény-számnál a pontbecslés megtévesztő; a mintaméretet a vizsgálat előtt kell jóváhagyni."]
    open(os.path.join(a.out, "T5-01_riport.md"), "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md[:8]))


if __name__ == "__main__":
    main()
