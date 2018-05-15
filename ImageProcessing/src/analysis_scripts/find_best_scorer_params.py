"""
Script for performing a near exhaustive search to find the best parameters
for the scorer. The parameters being optimised are:

SECTOR_THRESHOLD: The minimum percentage coverage of a sector to declare it as
                  covered by part of a stem cell.
NOISE_THRESHOLD: The value between 0 and 255 below which all pixels are
                 considered noise and set to 0.
"""

import cv2

import scorer

# Set how much weight is given to a score being exactly correct or within one of
# the correct score here.
EXACT_WEIGHTING = 10
ONE_OFF_WEIGHTING = 1

if __name__ == '__main__':
    # Path to directory of cells to be scored - should ideally be an argument.
    dirPath = 'img/sample_of_good_cells/'
    # Directory must contain a results.txt file with expected scores.
    expectedPath = dirPath + 'results.txt'
    expectedFile = open(expectedPath)
    expecteds = expectedFile.read().splitlines()
    max_score = 0
    best_sector_threshs = []
    best_noise_threshs = []
    for i in range(5, 60, 5):
        # Print to help track progress
        print(str(i))
        for j in range(0, 100, 4):
            score = 0
            scorer.set_params(i, j)
            out_of_images = False
            cnt = 0
            while not out_of_images:
                img = cv2.imread(dirPath + 'cells/' + str(cnt) + '.png')
                if img is not None:
                    expected = int(expecteds[cnt])
                    # Ignore rejected cells
                    if 9 > expected > 0:
                        actual = scorer.score(img)
                        difference = abs(expected - actual)
                        if difference == 0:
                            score += EXACT_WEIGHTING
                        elif difference == 1:
                            score += ONE_OFF_WEIGHTING
                    cnt += 1
                else:
                    out_of_images = True
            if score > max_score:
                max_score = score
                best_sector_threshs = [i]
                best_noise_threshs = [j]
            elif score >= max_score:
                best_sector_threshs.append(i)
                best_noise_threshs.append(j)
    # Output results
    print(str(max_score))
    for i, j in zip(best_sector_threshs, best_noise_threshs):
        print(str(i))
        print(str(j))
        print('--')
