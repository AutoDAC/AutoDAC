"""
Script for taking directories of images of (scored) cells and merging them
into one directory with each image uniquely numbered, and a new results file
with scores for all cells.
"""

import numpy as np
import os
from shutil import copyfile

TARGET_DIRS = ['img/to_merge_1/', 'img/to_merge_2/']
DEST_DIR = 'img/all_cells/'

if __name__ == '__main__':
    scores = []
    curr_img_scores = []
    tally = np.zeros((10,), np.uint32)
    cnt = 0
    for cellDir in TARGET_DIRS:
        resultsPath = cellDir + 'results.txt'
        resultsFile = open(resultsPath)
        results = resultsFile.read().splitlines()
        for i, result in enumerate(results):
            cellPath = cellDir + 'cells/' + str(i) + '.png'
            if os.path.isfile(cellPath):
                copyfile(cellPath, DEST_DIR + 'cells/' + str(cnt) + '.png')
                cnt += 1
                scores.append(result)
                tally[int(result)] += 1

    file = open(DEST_DIR + 'results.txt', 'w')
    for item in scores:
        file.write('%s\n' % item)
    file.close()
    # Write tally to file
    file = open(DEST_DIR + 'tally.txt', 'w')
    totalCells = np.ndarray.sum(tally) - tally[9]
    file.write('Number of cells of interest: %s\n' % totalCells)
    file.write('Number of rejects: %s\n' % tally[0])
    for i, score in enumerate(tally[1:]):
        file.write('Number of cells scoring ' + str(i + 1) + '/8: '
                   + str(score) + ' (' +
                   str(int((score / totalCells) * 100)) + '%)\n')
    file.close()
