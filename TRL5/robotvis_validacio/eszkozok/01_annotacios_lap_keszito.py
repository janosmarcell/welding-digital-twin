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
    fig.tight_layout(); fig.savefig(out_png, dpi=110); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--per-group", type=int, default=4); ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--exclude", default="", help="vesszővel elválasztott azonosítók (pl. g01_s10,g01_s30), amelyeket az annotátor már látott")
    a = ap.parse_args()
    rng = random.Random(a.seed)
    os.makedirs(os.path.join(a.out, "abrak"), exist_ok=True); os.makedirs(os.path.join(a.out, "csv_vak"), exist_ok=True)
    sheet, key, picked = [], [], []
    for gdir in sorted(glob.glob(os.path.join(a.dataset, "g0*"))):
        excl = {e.strip() for e in a.exclude.split(",") if e.strip()}
        files = [f for f in sorted(glob.glob(os.path.join(gdir, "*.csv"))) if os.path.basename(f)[:-4] not in excl]
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
        df.drop(columns=["TorchSignal"]).to_csv(os.path.join(a.out, "csv_vak", sid + ".csv"), index=True, index_label="sor", encoding="utf-8-sig")
        rel = os.path.relpath(f, a.dataset).replace(os.sep, "/")
        plot_file(df, os.path.join(a.out, "abrak", sid + ".png"), f"{sid} – {len(df)} sor; három varratot jelöljön meg időrendben")
        for k in (1, 2, 3):  # a kísérleti terv szerint darabonként három varrat készül
            sheet.append(dict(azonosito=f"{sid}_v{k}", csv_fajl=f"csv_vak/{sid}.csv", abra=f"abrak/{sid}.png", varrat_sorszam=k,
                              kezdet_sor="", veg_sor="", megjegyzes="", annotator="", datum=""))
            s, e = segs[k - 1] if k <= len(segs) else ("", "")
            key.append(dict(azonosito=f"{sid}_v{k}", auto_kezdet_sor=s, auto_veg_sor=e, auto_szakaszok_szama=len(segs)))
    pd.DataFrame(sheet).to_csv(os.path.join(a.out, "annotacio_sablon.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame(key).to_csv(os.path.join(a.out, "automata_kulcs.csv"), index=False, encoding="utf-8-sig")
    open(os.path.join(a.out, "ANNOTACIO_UTMUTATO.md"), "w", encoding="utf-8").write(
"""# T5-01 vak annotáció – útmutató az annotátornak

**Feladat:** minden kiválasztott hegesztési naplóban megjelölni a három varrat kezdő és záró sorát. Becsült idő: 2–3 óra.

**Amit kap:** `abrak/` (fájlonként egy ábra: a szerszám lépésköze, feszültség, áram, huzalsebesség a sorszám függvényében), `csv_vak/` (ugyanazok a naplók a TorchSignal oszlop nélkül, a `sor` oszlop a sorszám), `annotacio_sablon.csv` / `.xlsx` (ezt kell kitölteni).

**Fontos:** ne nyissa meg a tárolóban lévő eredeti CSV-ket és semmilyen „kulcs” fájlt, és ne beszélje meg az eredményt a kitöltés előtt senkivel. Ez teszi a vizsgálatot vakká.

## Lépések

1. Nyissa meg a sorhoz tartozó ábrát. Egy naplóban három varrat van, időrendben (`varrat_sorszam` 1, 2, 3).
2. A varrat **kezdete** ott van, ahol a szerszám lépésköze a varrat menti egyenletes, kis értékre (kb. 0,1–0,3 mm/sor) áll be, és az áram, feszültség, huzalsebesség a hegesztési szintre ugrik. A **vége** az utolsó sor, ahol ez még tart; utána a szerszám gyorsan elmozdul (nagy lépésköz), vagy az értékek leesnek.
3. Az ábrán keresse meg a helyet, majd a `csv_vak/` fájlban a `sor` oszlopból írja ki a pontos sorszámot a `kezdet_sor` és a `veg_sor` oszlopba.
4. Ha egy határ nem egyértelmű, hagyja üresen, és írja a `megjegyzes` oszlopba, miért. Ne becsüljön. Ha egy naplóban nem lát három varratot, azt is írja meg.
5. Töltse ki az `annotator` (név) és a `datum` oszlopot, mentse el, és adja vissza a fájlt a végrehajtónak.
""")
    print(f"{len(picked)} fájl, {len(sheet)} annotálandó varrat -> {a.out}")


if __name__ == "__main__":
    main()
