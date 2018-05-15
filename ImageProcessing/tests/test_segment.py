# test_segment.py
# Tests for image analysis end of the project

import shutil
import numpy as np
import cv2

from ImageProcessing.src.segment import *
from ImageProcessing.src.utils import create_or_wipe_dir

IMG_IN = 'ImageProcessing/tests/img/'
IMG_OUT = IMG_IN + 'cells/'


def test_segment_removes_cells_with_no_red():
    img = cv2.imread(IMG_IN + 'test_all_green.tiff')
    create_or_wipe_dir(IMG_OUT)
    cells_in_image = segment_region(img, IMG_OUT, 0, 200 / 512)
    shutil.rmtree(IMG_OUT)

    assert cells_in_image == 0


def test_segment_removes_cells_touching_edge():
    img = cv2.imread(IMG_IN + 'test_one_edge_cell_one_not.tiff')
    create_or_wipe_dir(IMG_OUT)
    cells_in_image = segment_region(img, IMG_OUT, 0, 120 / 187)
    shutil.rmtree(IMG_OUT)

    assert cells_in_image == 1


def test_merge_contours_simple():
    too_small = [full_contour[0:50], full_contour[50:]]
    merged = merge_contours(too_small, 455.88 / 913 * 455.88 / 913)
    assert len(merged) == 1
    assert np.array_equal(merged[0], full_contour)

full_contour = np.array([[[42, 21]],
                         [[41, 22]],
                         [[39, 22]],
                         [[38, 23]],
                         [[37, 23]],
                         [[36, 24]],
                         [[27, 24]],
                         [[26, 25]],
                         [[25, 25]],
                         [[24, 26]],
                         [[23, 26]],
                         [[22, 27]],
                         [[6, 27]],
                         [[5, 28]],
                         [[4, 28]],
                         [[2, 30]],
                         [[2, 31]],
                         [[1, 32]],
                         [[0, 32]],
                         [[0, 59]],
                         [[2, 59]],
                         [[6, 63]],
                         [[7, 63]],
                         [[9, 65]],
                         [[10, 65]],
                         [[14, 69]],
                         [[14, 72]],
                         [[13, 73]],
                         [[13, 79]],
                         [[12, 80]],
                         [[12, 84]],
                         [[13, 85]],
                         [[13, 86]],
                         [[15, 88]],
                         [[16, 88]],
                         [[17, 89]],
                         [[23, 89]],
                         [[24, 88]],
                         [[26, 88]],
                         [[27, 87]],
                         [[29, 87]],
                         [[30, 86]],
                         [[35, 86]],
                         [[36, 87]],
                         [[36, 96]],
                         [[38, 98]],
                         [[39, 98]],
                         [[44, 103]],
                         [[45, 103]],
                         [[46, 104]],
                         [[55, 104]],
                         [[58, 101]],
                         [[58, 98]],
                         [[59, 97]],
                         [[59, 96]],
                         [[61, 94]],
                         [[63, 94]],
                         [[64, 93]],
                         [[65, 93]],
                         [[66, 92]],
                         [[67, 92]],
                         [[68, 91]],
                         [[69, 91]],
                         [[70, 90]],
                         [[71, 90]],
                         [[75, 86]],
                         [[75, 85]],
                         [[77, 83]],
                         [[77, 82]],
                         [[78, 81]],
                         [[78, 79]],
                         [[79, 78]],
                         [[79, 74]],
                         [[80, 73]],
                         [[80, 72]],
                         [[83, 69]],
                         [[83, 68]],
                         [[85, 66]],
                         [[85, 63]],
                         [[86, 62]],
                         [[86, 52]],
                         [[85, 51]],
                         [[85, 48]],
                         [[84, 47]],
                         [[84, 46]],
                         [[83, 45]],
                         [[83, 44]],
                         [[82, 44]],
                         [[78, 40]],
                         [[78, 39]],
                         [[77, 38]],
                         [[77, 37]],
                         [[76, 36]],
                         [[76, 34]],
                         [[73, 31]],
                         [[62, 31]],
                         [[61, 32]],
                         [[58, 32]],
                         [[54, 28]],
                         [[54, 27]],
                         [[52, 25]],
                         [[52, 24]],
                         [[50, 22]],
                         [[49, 22]],
                         [[48, 21]]], dtype=np.int32)
