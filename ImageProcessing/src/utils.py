# Utility functions for image analysis

import numpy as np
import os
import re
import shutil


# Return a list of all image file paths in a given directory
def all_images_in_dir(dir_path):
    """
        Return all the image file paths in a given directory

        :param dir_path: Absolute path to directory
        :return: List of paths to images
    """
    return [dir_path + file for file in os.listdir(dir_path)
            if re.match(".*\.(tiff|tif|png|jpeg|jpg)", file)]


def create_or_wipe_dir(dir_path):
    """
        Create or wipe existing directory

        :param dir_path: Path of directory to create
        :return: None
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)


def print_scores(totals):
    """
        Print summary of scores

        :param totals: List of counts for each score
        :return: None
    """
    totalCells = np.ndarray.sum(totals)
    print('Number of cells of interest: ' + str(totalCells))
    if totalCells == 0:
        return
    print('Number of rejects: ' + str(totals[0]))
    for i, score in enumerate(totals[1:]):
        print('Number of cells scoring ' + str(i + 1) + '/8: ' + str(score)
              + ' (' + str(int((score / totalCells) * 100)) + '%)')
