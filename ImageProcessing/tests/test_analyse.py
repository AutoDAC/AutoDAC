# test_analyse.py
# Tests for image analysis end of the project

import cv2
import numpy as np
import pytest

from ImageProcessing.src.analyse import analyse_dir

IMG_IN = 'ImageProcessing/tests/img/'


def test_analyse_dir_rejects_invalid_dirs():
    with pytest.raises(ValueError):
        analyse_dir(IMG_IN + 'fake_directory/', 1)


# Waiting for Cora
# def test_segment_does_not_remove_cells_that_need_scoring():
#     analyse.analyse_dir('ImageProcessing/img/Tiffs_081117/')
#     passed = True
#     for search_img_path in utils.all_images_in_dir(
#             'ImageProcessing/img/img/Tiffs_081117_non_rejects/'):
#         found = False
#         search_key = cv2.imread(search_img_path)
#         for img_path in utils.all_images_in_dir(
#                 'ImageProcessing/img/Tiffs_081117/cells/'):
#             curr_img = cv2.imread(img_path)
#             if is_similar(search_key, curr_img):
#                 found = True
#                 break
#         if not found:
#             passed = False
#             sys.stderr.write(search_img_path + ' not found in segmented '
#                                                'images.\n')
#     assert passed
#
#
# def is_similar(img_1, img_2):
#     return img_1.shape == img_2.shape and \
#            not(np.bitwise_xor(img_1, img_2).any())
