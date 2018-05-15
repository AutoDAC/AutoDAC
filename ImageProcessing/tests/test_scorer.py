# test_py
# Unit tests for py
import cv2

from ImageProcessing.src.scorer import score

IMG_IN = 'ImageProcessing/tests/img/'

test_cells = []

for i in range(0, 9):
    test_cells.append(cv2.imread(IMG_IN + 'test_cell' + str(i) + '.png'))


def test_simple_0():
    score_value = score(test_cells[0])
    assert score_value == 0


def test_simple_1():
    score_value = score(test_cells[1])
    assert score_value == 1


def test_simple_2():
    score_value = score(test_cells[2])
    assert score_value == 2


def test_simple_3():
    score_value = score(test_cells[3])
    assert score_value == 3


def test_simple_4():
    score_value = score(test_cells[4])
    assert score_value == 4


def test_simple_5():
    score_value = score(test_cells[5])
    assert score_value == 5


def test_simple_6():
    score_value = score(test_cells[6])
    assert score_value == 6


def test_simple_7():
    score_value = score(test_cells[7])
    assert score_value == 7


def test_simple_8():
    score_value = score(test_cells[8])
    assert score_value == 8
