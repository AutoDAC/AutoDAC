# Module for assigning a score to an image of a cell

import numpy as np
import cv2

from ImageProcessing.src.preprocessor import prepare

WHITE = (255, 255, 255)
NOISE_THRESHOLD = 32
SECTOR_THRESHOLD = 20


def score(img):
    """
    Score an image

    :param img: RGB image data
    :return: Score of cell - in interval [0,8]
    """
    check_params(img)
    try:
        red = img[:, :, 2]
        green = img[:, :, 1].copy()
    except IndexError:
        raise TypeError('Images should be multidimensional numpy arrays. First'
                        'two dimensions are pixel coordinates. Grayscale images'
                        'have a single value at these coordinates, colour'
                        'images have another list containing BGR(A) values.')

    sectors_filled = [False] * 32

    # Threshold out low level background noise
    (_, red) = cv2.threshold(red, NOISE_THRESHOLD, 255,
                             cv2.THRESH_TOZERO)
    (h, w, _) = img.shape
    cx, cy = get_centroid(green)
    if cx is None:
        return 0
    centroid = (cx, cy)

    # Compute where sectors cross the image edges for 32 sectors of equal angle
    edgePoints = np.zeros((32, 2), dtype=np.int32)
    edgePoints[0] = (cx, 0)
    edgePoints[8] = (w, cy)
    edgePoints[16] = (cx, h)
    edgePoints[24] = (0, cy)
    edgePoints[1], edgePoints[17] = get_intersections(-4, cx, cy, h, w)
    edgePoints[2], edgePoints[18] = get_intersections(-2, cx, cy, h, w)
    edgePoints[3], edgePoints[19] = get_intersections(-4 / 3, cx, cy, h, w)
    edgePoints[4], edgePoints[20] = get_intersections(-1, cx, cy, h, w)
    edgePoints[5], edgePoints[21] = get_intersections(-3 / 4, cx, cy, h, w)
    edgePoints[6], edgePoints[22] = get_intersections(-1 / 2, cx, cy, h, w)
    edgePoints[7], edgePoints[23] = get_intersections(-1 / 4, cx, cy, h, w)

    edgePoints[9], edgePoints[25] = get_intersections(1 / 4, cx, cy, h, w)
    edgePoints[10], edgePoints[26] = get_intersections(1 / 2, cx, cy, h, w)
    edgePoints[11], edgePoints[27] = get_intersections(3 / 4, cx, cy, h, w)
    edgePoints[12], edgePoints[28] = get_intersections(1, cx, cy, h, w)
    edgePoints[13], edgePoints[29] = get_intersections(4 / 3, cx, cy, h, w)
    edgePoints[14], edgePoints[30] = get_intersections(2, cx, cy, h, w)
    edgePoints[15], edgePoints[31] = get_intersections(4, cx, cy, h, w)

    big_ellipse = cv2.ellipse2Poly((w // 2, h // 2), (w // 2, h // 2),
                                   0, 0, 360, 10)
    small_ellipse = cv2.ellipse2Poly((w // 2, h // 2), ((w // 16), (h // 16)),
                                     0, 0, 360, 10)
    ellipse_mask = np.zeros_like(red, np.uint8)
    cv2.fillPoly(ellipse_mask, [big_ellipse], 255)
    cv2.fillPoly(ellipse_mask, [small_ellipse], 0)

    for i, point in enumerate(edgePoints):
        triangle_mask = np.zeros_like(red, np.uint8)

        cv2.fillPoly(triangle_mask,
                     np.array([[edgePoints[i], edgePoints[(i + 1) % 32],
                                centroid]]), 255)
        sector_mask = cv2.bitwise_and(ellipse_mask, ellipse_mask,
                                      mask=triangle_mask)
        sector = cv2.bitwise_and(red, red, mask=sector_mask)
        try:
            areaRatio = np.count_nonzero(sector) / np.count_nonzero(sector_mask)
        except ZeroDivisionError:
            sectors_filled[i % 32] = False
            continue
        if areaRatio * 100 >= SECTOR_THRESHOLD:
            sectors_filled[i % 32] = True

    num_filled = sum(sectors_filled)

    return (num_filled + 1) // 4


def check_params(img):
    """
    Check image data contains 'ndim' attribute

    :param img: Image data
    :return: None
    """
    if not hasattr(img, 'ndim'):
        raise TypeError('Images should be numpy arrays')
    if img.ndim < 2 or img.ndim > 3:
        raise TypeError('Images should be multidimensional numpy arrays. First'
                        'two dimensions are pixel coordinates. Grayscale images'
                        'have a single value at these coordinates, colour'
                        'images have another list containing BGR(A) values.')


def get_centroid(green):
    """
    Find location of centroid in green image

    :param green: Image data
    :return: Co-ordinates of centre of centroid
    """
    binary = prepare(green)
    _, contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None, None
    m10 = 0
    m00 = 0
    m01 = 0
    for cnt in contours:
        moments = cv2.moments(cnt, binaryImage=True)
        m10 += moments['m10']
        m01 += moments['m01']
        m00 += moments['m00']

    cx = int(m10 / m00)
    cy = int(m01 / m00)
    return cx, cy


def get_intersections(m, cx, cy, h, w):
    """
    Find list of intersections between line cy = m*cx + c and box (0,0),(w,h)

    :param m: Gradient of line
    :param cx: X co-ordinate
    :param cy: Y co-ordinate
    :param h: Height of bounding box
    :param w: Width of bounding box
    :return: List of intersection co-ordinates
    """
    intersections = []
    reverse_list = False
    h -= 1
    w -= 1

    c = ((-m) * cx) + cy

    # Lines are y = 0, x = 0, y = h, x = w,
    # Top, y = 0
    top = np.array([-c / m, 0], dtype=np.float)
    if w > top[0] >= 0:
        intersections.append(top.astype(np.int32))
        if m > 0:
            reverse_list = True
    # Right, x = w
    right = np.array([w, m * w + c])
    if h > right[1] >= 0:
        intersections.append(right.astype(np.int32))
    # Bottom, y = h
    bottom = np.array([(h - c) / m, h])
    if w >= bottom[0] > 0:
        intersections.append(bottom.astype(np.int32))
    # Left, x = 0
    left = np.array([0, c])
    if h >= left[1] > 0:
        intersections.append(left.astype(np.int32))

    if reverse_list:
        intersections = intersections[1:] + intersections[:1]
    if len(intersections) > 2:
        if (abs(intersections[0][0] - intersections[1][0]) == 1 and
                intersections[0][1] == intersections[1][1]) or \
           (abs(intersections[0][1] - intersections[1][1]) == 1 and
                intersections[0][0] == intersections[1][0]):
            intersections.pop(1)
        if (abs(intersections[-1][0] - intersections[-2][0]) == 1 and
                intersections[-1][1] == intersections[-2][1]) or \
           (abs(intersections[-1][1] - intersections[-2][1]) == 1 and
                intersections[-1][0] == intersections[-2][0]):
            intersections.pop(-2)

    return intersections


def create_circular_masks(h, w, centroid, max_r):
    """
    Create circular mask

    :param h: Height of circle
    :param w: Width of circle
    :param centroid: Circle centre co-ordinates (x, y)
    :param max_r: Max radius of circle
    :return:
    """
    masks = []
    empty_img = np.zeros((h, w), dtype=np.uint8)
    inner_circle = np.copy(empty_img)
    cv2.circle(inner_circle, centroid, int(max_r / 5), WHITE, -1)
    for i in range(2, 6):
        curr_mask = np.copy(empty_img)
        cv2.circle(curr_mask, centroid, int(i * max_r / 5), WHITE, -1)
        inner_inv = cv2.bitwise_not(inner_circle)
        new_mask = cv2.bitwise_and(curr_mask, inner_inv)
        masks.append(new_mask)
        inner_circle = curr_mask
    return masks


def set_params(sector_thresh, noise_thresh):
    """
    Set sector threshold and noise thresholds

    :param sector_thresh: Sector threshold
    :param noise_thresh: Noise threshold
    :return: None
    """
    global SECTOR_THRESHOLD
    SECTOR_THRESHOLD = sector_thresh
    global NOISE_THRESHOLD
    NOISE_THRESHOLD = noise_thresh
