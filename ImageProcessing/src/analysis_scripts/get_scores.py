"""
Score a directory of cells and write the results to a file
"""

import cv2

import scorer

SECTOR_THRESHOLD = 25
NOISE_THRESHOLD = 32
CELL_DIR_PATH = 'img/all_cells/cells/'
RESULTS_FILE = 'img/actual_results.txt'

if __name__ == '__main__':
    out_of_images = False
    file = open(RESULTS_FILE, 'w')
    cnt = 0
    while not out_of_images:
        img = cv2.imread(CELL_DIR_PATH + str(cnt) + '.png')
        if img is not None:
            scorer.set_params(SECTOR_THRESHOLD, NOISE_THRESHOLD)
            score = scorer.score(img)
            file.write('%s ' % score)
            file.write('\n')
            cnt += 1
        else:
            out_of_images = True
    file.close()
