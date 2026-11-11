"""Automatikus varrat-szakaszolás, v2 (2026-11-11) – LEFAGYASZTVA az új vak annotáció előtt.

Miért kell: a v1 a szakasz végét a TorchSignal 1->0 váltásához tette. A TorchSignal az áramforrás
weboldaláról jön, és a T5-08 mérése szerint kb. 0,5 s-ot (4–5 sort) késik. A T5-01 első köre
(2026-11-11) ezt kimutatta: a varratvégeknél a v1 rendszeresen később jelzett, mint az annotátor.

A v2 szabálya (előre rögzítve, az annotációhoz nem hangolva):
  1. A varratokat továbbra is a TorchSignal azonosítja: minden 0->1 ... 1->0 szakasz egy varrat.
  2. Kezdet: változatlan, a TorchSignal 0->1 váltásának sora (a kezdetnél a robot áll, a késés
     nem számít, lásd a v1 eredményét).
  3. Vég: a robot pozíciójából, ami nem a weboldalról jön, ezért nem késik. A varrat vége az utolsó
     sor a robot elindulása előtt. Elindulás: az első olyan sor a szakasz kezdete után legalább
     MIN_HOSSZ sorral, ahol a szerszám lépésköze két egymást követő sorban is >= LEPES_MM.
     Ha a TorchSignal-szakasz vége ennél korábbi, a TorchSignal vége marad (a v2 csak korábbra hozhat).
  Paraméterek: LEPES_MM = 0,5 mm (az annotátori útmutató szerint hegesztés közben a lépésköz
  kb. 0,1–0,3 mm/sor, átálláskor ennek sokszorosa); MIN_HOSSZ = 10 sor.
"""
import numpy as np

LEPES_MM = 0.5
MIN_HOSSZ = 10
VALTOZAT = "v2-2026-11-11"


def torch_segments(on):
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


def step_mm(xyz):
    xyz = np.asarray(xyz, dtype=float)
    return np.r_[np.nan, np.sqrt((np.diff(xyz, axis=0) ** 2).sum(axis=1))]


def segments_v2(df):
    """(kezdet, vég) párok, 0-tól indexelt sorszámmal; df: a napló (X, Y, Z, TorchSignal oszloppal)."""
    st = step_mm(df[["X", "Y", "Z"]].to_numpy())
    out = []
    for s, e in torch_segments(df["TorchSignal"].to_numpy()):
        end = e
        for j in range(s + MIN_HOSSZ, min(e, len(st) - 2) + 1):
            if st[j] >= LEPES_MM and st[j + 1] >= LEPES_MM:
                end = min(e, j - 1)
                break
        out.append((s, end))
    return out
