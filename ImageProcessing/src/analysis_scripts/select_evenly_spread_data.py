"""
Select equal number of cells for each score to prevent skewed learning results.
"""
import numpy as np
import random
from shutil import copyfile

# Number of samples to be selected per score. Currently very low due to limited
# data for some scores.
NUM_OF_SAMPLES = 10

if __name__ == '__main__':
    allCellsDir = 'img/all_good_cells/'
    sampledDir = 'img/sample_of_good_cells/'
    scores = []
    tally = np.zeros((10,), np.uint32)
    resultsPath = allCellsDir + 'results.txt'
    resultsFile = open(resultsPath)
    results = resultsFile.read().splitlines()

    # Each index of 'indexes' array represents a score (1-8).
    # Array at each index contains the ids of the images that are given
    # that particular score.
    indexes = [[], [], [], [], [], [], [], []]
    for i, result in enumerate(results):
        indexes[int(result) - 1].append(i)

    samples = [[], [], [], [], [], [], [], []]
    for i in range(8):
        if len(indexes[i]) > NUM_OF_SAMPLES:
            samples[i] = random.sample(indexes[i], NUM_OF_SAMPLES)
        else:
            samples[i] = indexes[i]
        numSamples = len(samples[i])
        tally[i + 1] += numSamples

    cnt = 0
    for i, sampleSet in enumerate(samples):
        for sample in sampleSet:
            cellPath = allCellsDir + 'cells/' + str(sample) + '.png'
            copyfile(cellPath, sampledDir + 'cells/' + str(cnt) + '.png')
            cnt += 1
            scores.append(i + 1)

    file = open(sampledDir + 'results.txt', 'w')
    for item in scores:
        file.write('%s\n' % item)
    file.close()
    # Write tally to file
    file = open(sampledDir + 'tally.txt', 'w')
    totalCells = np.ndarray.sum(tally) - tally[9]
    file.write('Number of cells of interest: %s\n' % totalCells)
    file.write('Number of rejects: %s\n' % tally[0])
    for i, score in enumerate(tally[1:]):
        file.write('Number of cells scoring ' + str(i + 1) + '/8: '
                   + str(score) + ' (' +
                   str(int((score / totalCells) * 100)) + '%)\n')
    file.close()
