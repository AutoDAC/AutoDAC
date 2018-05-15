"""
Script for removing all rejects from the directory of scored cells. A cell is
meant to be scored 0 if it isn't large enough to warrant a score of 1 out of 8.
A score of 9 should be given if the image should not have been output by the
segmenter and is used to highlight problems with the segmenter.

9s are removed as they shouldn't be used to evaluate scorer performance (the
scorer should never have received them). We chose to remove 0s as at time of
writing our scorer never outputs 0 (to stop it from doing it too often).
Eventually 0 scores should be put back in.
"""

import os

if __name__ == '__main__':
    # Paths to directory of cell images and results files
    cellsPath = 'img/311217_2_no_rejects/cells/'
    resultsPath = 'img/Tiffs_311217_2_Results/results.txt'
    resultsFile = open(resultsPath)
    results = resultsFile.read().splitlines()
    for i, result in enumerate(results):
        if int(result) == 0 or int(result) == 9:
            cellPath = cellsPath + str(i) + '.png'
            if os.path.isfile(cellPath):
                os.remove(cellPath)
