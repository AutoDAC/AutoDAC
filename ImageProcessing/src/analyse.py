# Entry point to the image analysis program
import numpy as np
import cv2
from ImageProcessing.src.segment import segment_region
from ImageProcessing.src.utils import create_or_wipe_dir, print_scores, \
    all_images_in_dir
from ImageProcessing.src.scorer import score
import os


def analyse_img(img):
    """
        Segment and score a single image

        :param img: Loaded image to be scored (ie not a path)
        :return: An array of number of cells for each score - 0 to 8
    """
    cell_dir = 'cells/'
    create_or_wipe_dir(cell_dir)
    segment_region(img, cell_dir, 0, 1)

    totals = np.zeros((9,), np.uint32)
    for imgPath in all_images_in_dir(cell_dir):
        img = cv2.imread(imgPath)
        score_value = score(img)
        totals[score_value] += 1

    print_scores(totals)
    return totals


# Analyse a directory and print the results to stdout
def analyse_dir(dir_path, dist_per_pixel):
    """
        Segment and score every image in a directory

        :param dir_path: Path to directory containing images to be scored
        :param dist_per_pixel: Distance in µm represented by one pixel of an
        image in the given directory.
        :return: An array of number of cells for each score - 0 to 8
    """
    if not os.path.isdir(dir_path):
        raise ValueError('Invalid directory path')
    cell_dir = dir_path + 'cells/'
    create_or_wipe_dir(cell_dir)
    cnt = 0
    # Segment
    for imgPath in all_images_in_dir(dir_path):
        img = cv2.imread(imgPath)
        cnt = segment_region(img, cell_dir, cnt, dist_per_pixel)

    # Score
    totals = np.zeros((9,), np.uint32)
    for imgPath in all_images_in_dir(cell_dir):
        img = cv2.imread(imgPath)
        score_value = score(img)
        totals[score_value] += 1

    # print_scores(totals)
    return totals
