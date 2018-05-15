"""
Produces a confusion matrix for two sets of results, and outputs precision and
sensitivity scores. Precision and sensitivity are each calculated in two
different ways. The first is for exact matches where the expected and actual
score must be equal. The second is for where the expected and actual scores
must differ by at most 1.

Expects two arguments: a path to the file of expected scores, and a path to the
file of actual scores.

Both files should contain the same number of scores, one on each line, with the
scores from both files on a given line corresponding to the same image.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

# 0 to 8 inclusive
NUM_SCORES = 9

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        sys.stderr.write("Paths to expected and actual results not given")
        exit(1)
    expectedPath = str(sys.argv[1])
    actualPath = str(sys.argv[2])

    # Read results files into string arrays
    try:
        expectedFile = open(expectedPath)
        expecteds = expectedFile.read().splitlines()
        actualFile = open(actualPath)
        actuals = actualFile.read().splitlines()
    except FileNotFoundError:
        sys.stderr.write("Error opening a results file\n")
        exit(1)

    num_results = len(actuals)
    if len(expecteds) != num_results:
        sys.stderr.write("Different number of scores in expected and actual\n")
        exit(1)

    expected_tally = np.zeros((9,), np.uint32)
    actual_tally = np.zeros((9,), np.uint32)
    hcorrect_tally = np.zeros((9,), np.uint32)
    vcorrect_tally = np.zeros((9,), np.uint32)
    exact_correct_tally = np.zeros((9,), np.uint32)
    # Count occurances of each score
    confusion = np.zeros((NUM_SCORES, NUM_SCORES), np.float)
    for i in range(0, num_results):
        expected = int(expecteds[i])
        actual = int(actuals[i])
        expected_tally[expected] += 1
        actual_tally[actual] += 1
        if abs(expected - actual) <= 1:
            hcorrect_tally[expected] += 1
            vcorrect_tally[actual] += 1
        if expected == actual:
            exact_correct_tally[actual] += 1
        if (not (0 <= expected < NUM_SCORES) or
                not (0 <= actual < NUM_SCORES)):
            sys.stderr.write("Unexpected score at line " + str(i + 1) + '\n')
            exit(1)
        confusion[expected][actual] += 1

    # Normalise rows so they sum to 1
    for row in confusion:
        rowSum = sum(row)
        if rowSum != 0:
            for i in range(0, len(row)):
                row[i] /= rowSum

    # Output precision and sensitivity scores
    for i in range(1, 9):
        sensitivity = 0
        precision = 0
        if expected_tally[i] != 0:
            sensitivity = hcorrect_tally[i] / expected_tally[i]
        if actual_tally[i] != 0:
            precision = vcorrect_tally[i] / actual_tally[i]
        print('For cells scoring ' + str(i) + ':')
        print('Sensitivity = ' + "%.2f" % sensitivity)
        print('Precision = ' + "%.2f" % precision)
        print('')
    print('Exact statistics:')
    for i in range(1, 9):
        sensitivity = 0
        precision = 0
        if expected_tally[i] != 0:
            sensitivity = exact_correct_tally[i] / expected_tally[i]
        if actual_tally[i] != 0:
            precision = exact_correct_tally[i] / actual_tally[i]
        print('For cells scoring ' + str(i) + ':')
        print('Sensitivity = ' + "%.2f" % sensitivity)
        print('Precision = ' + "%.2f" % precision)
        print('')

    plt.matshow(confusion, vmin=0, vmax=1)
    plt.xticks(np.arange(0, 9))
    plt.yticks(np.arange(0, 9))
    plt.xlabel('Actual', fontsize=18)
    plt.ylabel('Expected', fontsize=18)
    plt.colorbar()
    plt.show()
