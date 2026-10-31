#!/usr/bin/env python3
"""
recompute_trl_numbers.py – a TRL 4 dokumentumban idézett "B" osztályú számok újraszámolása a tároló nyers adataiból.

Használat (a tároló gyökeréből):
    python3 tools/trl_recompute/recompute_trl_numbers.py --repo . --out trl_numbers_out

Csak olvassa a tárolót; a kimenet a --out mappába kerül. Függőség: numpy, pandas.
A szkript nem módosítja az adatokat, és nem tartalmaz hálózati hívást.

Kimenet:
  trl_numbers.json        az összes idézett szám
  csv_segment_summary.csv aktív varratszakaszonkénti jellemzők
  csv_file_summary.csv    fájlonkénti jellemzők
  coverage_150.csv        a 150 darab lefedettsége modalitásonként
"""
import argparse, glob, json, os
from datetime import datetime, timezone
import numpy as np
import pandas as pd

COLS = ["SysTimeMsecs", "X", "Y", "Z", "Rx", "Ry", "Rz", "TorchSignal", "Voltage", "Current", "WireFeedSpeed"]
NOM = {"g01_30": 30, "g02_40": 40, "g03_50": 50, "g04_60": 60, "g05_70": 70}


def active_segments(on):
    d = np.diff(np.concatenate([[0], on, [0]]))
    return np.where(d == 1)[0], np.where(d == -1)[0]  # a vég index kizáró


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    ds = os.path.join(a.repo, "datasets", "welding_experiments_v1")
    imgs = os.path.join(a.repo, "datasets", "welding_seam_images_v1")
    os.makedirs(a.out, exist_ok=True)

    files = sorted(glob.glob(os.path.join(ds, "g0*", "*.csv")))
    frows, srows, mid = [], [], []
    for f in files:
        sid = os.path.basename(f)[:-4]
        grp = os.path.basename(os.path.dirname(f))
        df = pd.read_csv(f, encoding="utf-8-sig")
        t = df["SysTimeMsecs"].to_numpy(dtype=np.int64)
        on = (df["TorchSignal"].to_numpy() > 0).astype(int)
        st, en = active_segments(on)
        xyz = df[["X", "Y", "Z"]].to_numpy(dtype=float)
        frows.append(dict(sample=sid, group=grp, columns_ok=list(df.columns) == COLS, rows=len(df), nan_cells=int(df.isna().sum().sum()),
                          t_first_utc=datetime.fromtimestamp(t[0] / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                          duration_s=(t[-1] - t[0]) / 1000, dup_timestamp_share=float((np.diff(t) == 0).mean()),
                          nonmonotonic=bool((np.diff(t) < 0).any()), segments=len(st)))
        for k, (s, e) in enumerate(zip(st, en), start=1):
            seg = df.iloc[s:e]
            step = np.linalg.norm(np.diff(xyz[s:e], axis=0), axis=1) if e - s > 1 else np.array([0.0])
            srows.append(dict(sample=sid, group=grp, seg=k, dur_s=(t[e - 1] - t[s]) / 1000, path_mm=float(step.sum()),
                              V_med=float(seg["Voltage"].median()), I_med=float(seg["Current"].median()), WFS_med=float(seg["WireFeedSpeed"].median()),
                              speed_cm_min=(step.sum() / 10) / (((t[e - 1] - t[s]) / 1000) / 60) if t[e - 1] > t[s] else np.nan))
            # a szakasz középső felének haladási sebessége, az ismétlődő időbélyegek kiszűrése után
            tt, pp = t[s:e], xyz[s:e]
            idx = np.r_[0, np.where(np.diff(tt) > 0)[0] + 1]
            if len(idx) < 8:
                continue
            v = np.linalg.norm(np.diff(pp[idx], axis=0), axis=1) / (np.diff(tt[idx]) / 1000) * 6.0  # mm/s -> cm/perc
            n = len(v)
            mid.append((grp, float(np.median(v[n // 4: 3 * n // 4]))))
    F, S = pd.DataFrame(frows), pd.DataFrame(srows)
    Mid = pd.DataFrame(mid, columns=["group", "v"])
    F.to_csv(os.path.join(a.out, "csv_file_summary.csv"), index=False)
    S.to_csv(os.path.join(a.out, "csv_segment_summary.csv"), index=False)

    res = {}
    res["csv_files"] = len(F)
    res["columns_ok_all"] = bool(F.columns_ok.all())
    res["nan_cells_total"] = int(F.nan_cells.sum())
    res["rows_total"] = int(F.rows.sum())
    res["rows_min_median_max"] = [int(F.rows.min()), float(F.rows.median()), int(F.rows.max())]
    res["duration_s_min_max"] = [float(F.duration_s.min()), float(F.duration_s.max())]
    res["segments_total"] = len(S)
    res["files_not_3_segments"] = F.loc[F.segments != 3, "sample"].tolist()
    res["timestamp_dup_share_min_max"] = [float(F.dup_timestamp_share.min()), float(F.dup_timestamp_share.max())]
    res["timestamps_nonmonotonic_files"] = int(F.nonmonotonic.sum())
    res["recording_dates_utc_if_unix_ms"] = sorted(set(F.t_first_utc.str[:10]))
    res["path_mm_median"] = float(S.path_mm.median())
    res["path_mm_quartiles"] = [float(S.path_mm.quantile(.25)), float(S.path_mm.quantile(.75))]
    res["path_mm_max"] = float(S.path_mm.max())
    res["path_37_43_share"] = float(((S.path_mm >= 37) & (S.path_mm <= 43)).mean())
    res["V_med_range"] = [float(S.V_med.min()), float(S.V_med.max())]
    res["I_med_range"] = [float(S.I_med.min()), float(S.I_med.max())]
    res["WFS_med_range"] = [float(S.WFS_med.min()), float(S.WFS_med.max())]
    grp = {}
    for g, n in NOM.items():
        s, m = S[S.group == g], Mid[Mid.group == g].v
        s1 = s[s.seg == 1].copy()
        s1["idx"] = s1["sample"].str.extract(r"_s(\d+)").astype(int)
        grp[g] = dict(segments=len(s), nominal=n, mid_speed_median=float(m.median()), mid_speed_dev_pct=float((m.median() / n - 1) * 100),
                      whole_segment_speed_dev_pct=float((s.speed_cm_min.median() / n - 1) * 100),
                      V_range=[float(s.V_med.min()), float(s.V_med.max())], I_range=[float(s.I_med.min()), float(s.I_med.max())],
                      spearman_I=float(s1.idx.corr(s1.I_med, method="spearman")), spearman_V=float(s1.idx.corr(s1.V_med, method="spearman")),
                      spearman_WFS=float(s1.idx.corr(s1.WFS_med, method="spearman")))
    res["groups"] = grp

    # ---- lefedettség és leképezés
    M = pd.read_csv(os.path.join(imgs, "manifest.csv"), encoding="utf-8-sig")
    res["pano_images_total"] = len(M)
    res["pano_images_in_150_seams_1_3"] = int(M[(M.darab_id.between(1, 150)) & (M.varrat_sorszam.between(1, 3))].shape[0])
    res["pano_images_outside"] = int(len(M) - res["pano_images_in_150_seams_1_3"])
    res["pano_json_images"] = int(M.aram_A.notna().sum())
    ply = {}
    for f in glob.glob(os.path.join(ds, "g0*", "*.ply")):
        with open(f, "rb") as fh:
            hdr = fh.read(400).decode("latin1")
        nv = int([l for l in hdr.splitlines() if l.startswith("element vertex")][0].split()[-1])
        ply[os.path.basename(f)[:-4]] = ("mesh_vcglib" if "VCGLIB" in hdr else "cloud_revopoint" if "revopoint" in hdr.lower() else "other", nv)
    res["ply_counts"] = {k: sum(1 for v in ply.values() if v[0] == k) for k in ("mesh_vcglib", "cloud_revopoint", "other")}
    res["ply_vertices_mesh_min_max"] = [min(v[1] for v in ply.values() if v[0] == "mesh_vcglib"), max(v[1] for v in ply.values() if v[0] == "mesh_vcglib")]
    res["ply_vertices_cloud_min_max"] = [min(v[1] for v in ply.values() if v[0] == "cloud_revopoint"), max(v[1] for v in ply.values() if v[0] == "cloud_revopoint")]
    S["piece"] = S["sample"].str.extract(r"_s(\d+)").astype(int)
    rows = []
    for sid in F["sample"]:
        p = int(sid.split("_s")[1])
        sub = M[(M.darab_id == p) & (M.varrat_sorszam.between(1, 3))]
        rows.append(dict(sample=sid, piece=p, pano_seams=int(sub.varrat_sorszam.nunique()), ply=ply.get(sid, ("", 0))[0]))
    C = pd.DataFrame(rows)
    C.to_csv(os.path.join(a.out, "coverage_150.csv"), index=False)
    res["pieces_with_pano_all3"] = int((C.pano_seams == 3).sum())
    res["pieces_without_pano"] = C.loc[C.pano_seams == 0, "sample"].tolist()
    res["pieces_with_ply"] = int((C.ply != "").sum())
    res["pieces_all_three_modalities"] = int(((C.pano_seams > 0) & (C.ply != "")).sum())
    res["ply_without_pano"] = C.loc[(C.ply != "") & (C.pano_seams == 0), "sample"].tolist()
    J = M[M.aram_A.notna() & (M.darab_id <= 150)].merge(S, left_on=["darab_id", "varrat_sorszam"], right_on=["piece", "seg"], how="inner")
    res["mapping_n"] = len(J)
    res["mapping_pearson_current"] = float(np.corrcoef(J.aram_A, J.I_med)[0, 1])
    sh = {}
    for k in (-5, -2, -1, 1, 2, 5):
        J2 = M[M.aram_A.notna() & (M.darab_id <= 150)].copy()
        J2["p2"] = J2.darab_id + k
        K = J2.merge(S, left_on=["p2", "varrat_sorszam"], right_on=["piece", "seg"], how="inner")
        sh[str(k)] = float(np.corrcoef(K.aram_A, K.I_med)[0, 1])
    res["mapping_pearson_shifted_id"] = sh
    with open(os.path.join(a.out, "trl_numbers.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
