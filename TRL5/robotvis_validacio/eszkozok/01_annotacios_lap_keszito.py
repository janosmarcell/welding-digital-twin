#!/usr/bin/env python3
"""T5-01: vak annotációs lap készítése a varratkezdő/-záró események ellenőrzéséhez.

A lap a kiválasztott CSV-fájlokhoz ábrát készít (feszültség, áram, huzalsebesség, a szerszám soronkénti lépésköze),
a TorchSignal oszlop NÉLKÜL, hogy az annotátor ne lássa az automatikus eredményt.
Az automatikus szakaszhatárok külön kulcsfájlba kerülnek (csak a kiértékelő használja).

Használat:
  python3 -I 01_annotacios_lap_keszito.py --dataset <repo>/datasets/welding_experiments_v1 --out <kimeneti_mappa> [--per-group 4] [--seed 1]
"""
import argparse, glob, os, random, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLS = ["SysTimeMsecs", "X", "Y", "Z", "Rx", "Ry", "Rz", "TorchSignal", "Voltage", "Current", "WireFeedSpeed"]


def active_segments(on):
    """A TorchSignal 0->1 és 1->0 átmenete közötti szakaszok: (kezdő sor, utolsó bekapcsolt sor), 0-tól indexelve."""
    on = np.asarray(on) > 0
    segs, start = [], None
    for i, v in enumerate(on):
        if v and start is None:
            start = i
        elif not v and start is not None:
            segs.append((start, i - 1)); start = None
    if start is not None:
        segs.append((start, len(on) - 1))
    return segs


def plot_file(df, out_png, title):
    n = len(df)
    xyz = df[["X", "Y", "Z"]].to_numpy(float)
    step = np.r_[0.0, np.linalg.norm(np.diff(xyz, axis=0), axis=1)]  # a szerszám lépésköze sorról sorra [mm]
    rows = np.arange(n)
    fig, ax = plt.subplots(4, 1, figsize=(15, 9), sharex=True)
    for a, y, lab in zip(ax, (step, df["Voltage"], df["Current"], df["WireFeedSpeed"]),
                         ("Szerszám lépésköze soronként [mm] (szimlog)", "Feszültség [V]", "Áram [A]", "Huzalsebesség [m/min]")):
        a.plot(rows, y, lw=1.1); a.set_ylabel(lab, fontsize=9); a.grid(True, which="both", alpha=.35)
        a.set_xticks(np.arange(0, n + 1, 50)); a.set_xticks(np.arange(0, n + 1, 10), minor=True)
    ax[0].set_yscale("symlog", linthresh=0.1); ax[0].set_ylim(0, max(1.0, float(np.percentile(step, 99.5))))
    ax[-1].set_xlabel("Sor (0-tól indexelve, a fejléc nem számít)")
    ax[0].set_title(title, fontsize=11)
    fig.tight_layout(); fig.savefig(out_png, dpi=80); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--per-group", type=int, default=4); ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    os.makedirs(os.path.join(a.out, "abrak"), exist_ok=True)
    sheet, key, picked = [], [], []
    for gdir in sorted(glob.glob(os.path.join(a.dataset, "g0*"))):
        files = sorted(glob.glob(os.path.join(gdir, "*.csv")))
        chosen = set(rng.sample(files, min(a.per_group, len(files))))
        # a g02_s33 (két aktív szakasz) kivételt mindig bevesszük, ha van
        chosen |= {f for f in files if os.path.basename(f) == "g02_s33.csv"}
        picked += sorted(chosen)
    for f in picked:
        sid = os.path.basename(f)[:-4]
        df = pd.read_csv(f, encoding="utf-8-sig")
        if list(df.columns) != COLS:
            sys.exit(f"Váratlan oszlopok: {f}")
        segs = active_segments(df["TorchSignal"].to_numpy())
        rel = os.path.relpath(f, a.dataset).replace(os.sep, "/")
        plot_file(df, os.path.join(a.out, "abrak", sid + ".png"), f"{sid} – {len(df)} sor; három varratot jelöljön meg időrendben")
        for k in (1, 2, 3):  # a kísérleti terv szerint darabonként három varrat készül
            sheet.append(dict(azonosito=f"{sid}_v{k}", csv_fajl=rel, abra=f"abrak/{sid}.png", varrat_sorszam=k,
                              kezdet_sor="", veg_sor="", megjegyzes="", annotator="", datum=""))
            s, e = segs[k - 1] if k <= len(segs) else ("", "")
            key.append(dict(azonosito=f"{sid}_v{k}", auto_kezdet_sor=s, auto_veg_sor=e, auto_szakaszok_szama=len(segs)))
    pd.DataFrame(sheet).to_csv(os.path.join(a.out, "annotacio_sablon.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame(key).to_csv(os.path.join(a.out, "automata_kulcs.csv"), index=False, encoding="utf-8-sig")
    open(os.path.join(a.out, "ANNOTACIO_UTMUTATO.md"), "w", encoding="utf-8").write(
"""# T5-01 annotációs útmutató

Az `annotacio_sablon.csv` minden sorához tartozik egy ábra (`abrak/`). Az ábra a feszültséget, az áramot, a huzalsebességet és a szerszám soronkénti lépésközét mutatja a CSV soraihoz (0-tól indexelve) – a TorchSignal oszlopot szándékosan nem.

1. Nyissa meg a sorhoz tartozó ábrát. A fájlban három varrat van; a `varrat_sorszam` az időrendi sorrendet adja (1 = első).
2. `kezdet_sor`: az első sor, ahol a varrat készítése megkezdődik (az ív begyújt: az áram/feszültség/huzalsebesség felfut, és a szerszám a varrat mentén elindul).
3. `veg_sor`: az utolsó sor, ahol a varratot még készíti (az ív kialszik, az áram/huzalsebesség lecsökken).
4. Ha egy varratnál nem egyértelmű az esemény, hagyja üresen a mezőt, és írja a `megjegyzes` oszlopba, miért. Ne becsüljön.
5. Töltse ki az `annotator` és a `datum` oszlopot. A kulcsfájlt (`automata_kulcs.csv`) ne nyissa meg a kitöltés előtt.
6. Opcionális, de ajánlott: a robotprogram ARCON/ARCOF sorai vagy videó alapján ellenőrizze a határokat.

A kiértékelés: `02_annotacio_kiertekelo.py --kulcs automata_kulcs.csv --kitoltott annotacio_sablon.csv --out <mappa>`.
""")
    print(f"{len(picked)} fájl, {len(sheet)} annotálandó varrat -> {a.out}")


if __name__ == "__main__":
    main()
