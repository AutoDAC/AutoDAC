# test_scorer.py
# Unit tests for scorer.py
import numpy as np

from ImageProcessing.src.scorer import get_intersections


def test_top_right():
    h = 8
    w = 10
    cx = 7
    cy = 2
    m = 2
    intersections = get_intersections(m, cx, cy, h, w)
    assert len(intersections) == 2
    assert np.array_equal(intersections[0], [9, 6])
    assert np.array_equal(intersections[1], [6, 0])


def test_right_bottom():
    h = 8
    w = 20
    cx = 13
    cy = 5
    m = -1 / 4
    intersections = get_intersections(m, cx, cy, h, w)
    assert len(intersections) == 2
    assert np.array_equal(intersections[0], [19, 3])
    assert np.array_equal(intersections[1], [5, 7])


def test_bottom_left():
    h = 14
    w = 20
    cx = 5
    cy = 9
    m = 1
    intersections = get_intersections(m, cx, cy, h, w)
    assert len(intersections) == 2
    assert np.array_equal(intersections[0], [9, 13])
    assert np.array_equal(intersections[1], [0, 4])


def test_left_top():
    h = 10
    w = 10
    cx = 3
    cy = 2
    m = -2
    intersections = get_intersections(m, cx, cy, h, w)
    assert len(intersections) == 2
    assert np.array_equal(intersections[0], [4, 0])
    assert np.array_equal(intersections[1], [0, 8])


def test_top_bottom():
    h = 10
    w = 10
    cx = 5
    cy = 5
    m = 4
    intersections = get_intersections(m, cx, cy, h, w)
    assert len(intersections) == 2
    assert np.array_equal(intersections[0], [6, 9])
    assert np.array_equal(intersections[1], [3, 0])


def test_right_left():
    h = 10
    w = 10
    cx = 5
    cy = 5
    m = -3 / 4
    intersections = get_intersections(m, cx, cy, h, w)
    assert len(intersections) == 2
    assert np.array_equal(intersections[0], [9, 2])
    assert np.array_equal(intersections[1], [0, 8])


def test_top_left_corner():
    h = 5
    w = 7
    cx = 2
    cy = 2
    m = 1
    intersections = get_intersections(m, cx, cy, h, w)
    assert len(intersections) == 2
    assert np.array_equal(intersections[0], [4, 4])
    assert np.array_equal(intersections[1], [0, 0])


def test_top_right_corner():
    h = 7
    w = 5
    cx = 2
    cy = 2
    m = -1
    intersections = get_intersections(m, cx, cy, h, w)
    assert len(intersections) == 2
    assert np.array_equal(intersections[0], [4, 0])
    assert np.array_equal(intersections[1], [0, 4])


def test_bottom_left_corner():
    h = 7
    w = 5
    cx = 2
    cy = 2
    m = -2
    intersections = get_intersections(m, cx, cy, h, w)
    assert len(intersections) == 2
    assert np.array_equal(intersections[0], [3, 0])
    assert np.array_equal(intersections[1], [0, 6])


def test_bottom_right_corner():
    h = 6
    w = 7
    cx = 4
    cy = 4
    m = 1 / 2
    intersections = get_intersections(m, cx, cy, h, w)
    assert len(intersections) == 2
    assert np.array_equal(intersections[0], [6, 5])
    assert np.array_equal(intersections[1], [0, 2])
