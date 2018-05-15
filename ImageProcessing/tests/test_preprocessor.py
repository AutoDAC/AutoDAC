# test_py
import cv2
import numpy as np
import pytest

from ImageProcessing.src.preprocessor import prepare


img = cv2.imread('ImageProcessing/tests/img/test_region.tif')


def test_rejects_non_images():
    with pytest.raises(TypeError):
        prepare(np.zeros(9))
    with pytest.raises(TypeError):
        prepare(0)


def test_rejects_invalid_blur_radius():
    with pytest.raises(ValueError):
        prepare(img, blur_radius=20)
    with pytest.raises(ValueError):
        prepare(img, blur_radius=3.2)
    with pytest.raises(ValueError):
            prepare(img, blur_radius=-1)
    with pytest.raises(TypeError):
        prepare(img, blur_radius='wide')


def test_rejects_invalid_noise_thresh():
    with pytest.raises(TypeError):
        prepare(img, noise_thresh='high')
