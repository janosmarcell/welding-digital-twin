"""Reproducibility checks run with: python -m pytest src/test_validation.py -q"""
import numpy as np
from synthetic_v1 import make_baseline,segments,make_2d,image_quality,synthetic_3d,point_distances,classify_workpiece

def test_segments():
    frame,expected=make_baseline()
    assert segments(frame.TorchSignal)==expected

def test_image_qc():
    clean,corrupted=make_2d()
    assert image_quality(clean)['is_evaluable']
    assert not image_quality(corrupted)['is_evaluable']

def test_missing_data_cannot_be_ok():
    assert classify_workpiece(True,False,True)=='ELLENORIZENDO'
    assert classify_workpiece(False,True,True)=='ELLENORIZENDO'
    assert classify_workpiece(True,True,False)=='ELLENORIZENDO'

def test_synthetic_defect_is_not_no_defect():
    reference,defective,truth=synthetic_3d()
    distances=point_distances(reference,defective)
    assert np.median(distances[truth])>np.median(distances[~truth])
