#!/usr/bin/env python3
"""T5-08 kiértékelő: a RobotVis késleltetés- és adatvesztés-naplójának kiértékelése.

Bemenet: CSV oszlopai: run_id, seq, t_recv_ms, t_display_ms  (azonos órán mért, milliszekundumban; lásd robotvis_latency_logger.py)
Használat:
  python3 -I 03_keses_kiertekelo.py --log robotvis_latency.csv --out <mappa> [--cel-ms 2000] [--min-futas 3]
"""
import argparse, os
import numpy as np
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--cel-ms", type=float, default=2000.0); ap.add_argument("--min-futas", type=int, default=3)
    ap.add_argument("--megallas-ms", type=float, default=2000.0, help="ennél hosszabb kijelzési szünet megállásnak számít")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    d = pd.read_csv(a.log)
    d["kesleltetes_ms"] = d["t_display_ms"] - d["t_recv_ms"]
    rows = []
    for rid, g in d.groupby("run_id"):
        g = g.sort_values("seq")
        lat = g["kesleltetes_ms"].to_numpy()
        seq = g["seq"].to_numpy()
        expected = int(seq.max() - seq.min() + 1); lost = expected - len(np.unique(seq))
        gaps = np.diff(np.sort(g["t_display_ms"].to_numpy()))
        rows.append(dict(run_id=rid, csomag=len(g), elveszett=lost, elveszett_arany=lost / expected if expected else np.nan,
                         P50_ms=np.percentile(lat, 50), P95_ms=np.percentile(lat, 95), P99_ms=np.percentile(lat, 99), max_ms=lat.max(),
                         cel_alatt_arany=float((lat <= a.cel_ms).mean()), megallasok=int((gaps > a.megallas_ms).sum()),
                         negativ_kesleltetes=int((lat < 0).sum())))
    r = pd.DataFrame(rows); r.to_csv(os.path.join(a.out, "T5-08_futasok.csv"), index=False, encoding="utf-8-sig")
    allp95 = np.percentile(d["kesleltetes_ms"], 95)
    ok = len(r) >= a.min_futas and (r["P95_ms"] <= a.cel_ms).all() and (r["negativ_kesleltetes"] == 0).all()
    verdict = ("A KAPU TELJESÜL" if ok else ("KEVÉS FUTÁS" if len(r) < a.min_futas else "A KAPU NEM TELJESÜL"))
    md = ["# T5-08 eredmény (szoftveres késleltetés)", "",
          f"- Futások száma: {len(r)} (követelmény: ≥ {a.min_futas}); összes csomag: {len(d)}",
          f"- Összevont P95: {allp95:.0f} ms; cél: P95 ≤ {a.cel_ms:.0f} ms minden futásban (jóváhagyandó)",
          f"- Összes elveszett csomag: {int(r['elveszett'].sum())}; kijelzési megállás (> {a.megallas_ms:.0f} ms): {int(r['megallasok'].sum())}",
          f"- **{verdict}** (csak a késleltetési feltételre; az adatvesztést és a kijelzési megállásokat a jegyzőkönyvben külön értékelni kell)", "", r.round(3).to_string(index=False), "",
          "Megjegyzés: ez a mérés a RobotVis vétele és kijelzése közötti szoftveres késleltetést adja. A robot és a hegesztőforrás felől érkező",
          "késleltetést (a vezérlő/webes felület lekérdezési ideje) külön kell mérni (pl. képernyőfelvétel a kijelzővel és a vezérlőpulttal együtt)."]
    open(os.path.join(a.out, "T5-08_riport.md"), "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md[:7]))


if __name__ == "__main__":
    main()
