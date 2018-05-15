"""
Locate individual cells in image of many cellas
"""
# Segment cells only, don't analyse
import numpy as np
import cv2
import sys
import ImageProcessing.src.utils as utils
import os

BR_DEF = 21
NT_MIN = 14
MIN_AREA = 2500
MAX_AREA = 3600
WHITE = (255, 255, 255)


def segment_region(img, out_path, cnt, dist_per_pixel):
    """
    Find regions containing cells in the image

    :param img: Image object
    :param dist_per_pixel: How big wide each pixel is
    :return: List of regions
    """
    area_per_pixel = dist_per_pixel * dist_per_pixel
    img_h, img_w = img.shape[:2]
    green = img[:, :, 1]
    blurred = cv2.GaussianBlur(green, (BR_DEF, BR_DEF), 0)
    # Apply a threshold to remove background noise
    _, remaining = cv2.threshold(blurred, NT_MIN, 0, cv2.THRESH_TOZERO)

    contours = []
    noise_thresh = NT_MIN
    while np.any(remaining):
        # DEBUGGING
        # cv2.imwrite('img/remaining.png', remaining)
        # END
        _, remaining = cv2.threshold(remaining, noise_thresh,
                                     0, cv2.THRESH_TOZERO)
        _, prepared = cv2.threshold(remaining, noise_thresh, 255,
                                    cv2.THRESH_BINARY)
        _, remaining_contours, _ = cv2.findContours(prepared, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_SIMPLE)
        too_small = []
        for contour in remaining_contours:
            # # DEBUGGING CODE ONLY - VERY SLOW
            # cpy = img.copy()
            # cv2.drawContours(cpy, [contour], -1, WHITE)
            # cv2.imwrite('img/cntr.png', cpy)

            # Determine smallest rectangle that surrounds contour
            x, y, w, h = cv2.boundingRect(contour)

            # Ignore cells touching edges
            if x == 0 or y == 0 or x + w == img_w or y + h == img_h:
                cv2.drawContours(remaining, [contour], 0, 0)
                cv2.fillPoly(remaining, [contour], 0)
                # when dealing with images containing only one cell,
                # the cell might touch the edge
                continue

            area = w * h * area_per_pixel
            if int(1.4 * MAX_AREA) <= area:
                continue
            elif int(0.1 * MIN_AREA) <= area:
                cv2.drawContours(remaining, [contour], 0, 0)
                cv2.fillPoly(remaining, [contour], 0)
                if area <= int(0.6 * MIN_AREA):
                    too_small.append(contour)
                else:
                    contours.append(contour)
            else:
                cv2.drawContours(remaining, [contour], 0, 0)
                cv2.fillPoly(remaining, [contour], 0)

        contours += merge_contours(too_small, area_per_pixel)
        noise_thresh += 6

    # Output the contours found
    for contour in contours:

        x, y, w, h = cv2.boundingRect(contour)
        crypt = img[y: y + h, x: x + w].copy()

        red_part = crypt[:, :, 2]
        grn_chnl = crypt[:, :, 1]
        centre_y = h // 2
        centre_x = w // 2
        grn_cntr = grn_chnl[centre_y - centre_y // 2: centre_y + centre_y // 2,
                            centre_x - centre_x // 2: centre_x + centre_x // 2]

        _, red_nse_rmvd = cv2.threshold(red_part, 40, 255,
                                        cv2.THRESH_TOZERO)
        _, grn_nse_rmvd = cv2.threshold(grn_cntr, 20, 255,
                                        cv2.THRESH_TOZERO)
        # Red must account for > 2% of area to be considered significant

        if cv2.countNonZero(red_nse_rmvd) > (w * h) / 20 and \
                cv2.countNonZero(grn_nse_rmvd) > (w * h) / 16:

            SCORING_AREA = 0.2
            x_to_score = max(0, int(x - SCORING_AREA * w))
            y_to_score = max(0, int(y - SCORING_AREA * h))
            w_to_score = min(img_w - x_to_score,
                             int(w * (1 + 2 * SCORING_AREA)))
            h_to_score = min(img_h - y_to_score,
                             int(h * (1 + 2 * SCORING_AREA)))

            # Extract area we want our scorer to see
            cell_to_score = img[y_to_score: y_to_score + h_to_score,
                                x_to_score: x_to_score + w_to_score].copy()
            scoring_mask = np.zeros_like(cell_to_score)
            half_w = w_to_score // 2
            half_h = h_to_score // 2
            ellipse = cv2.ellipse2Poly((half_w, half_h), (half_w, half_h),
                                       0, 0, 360, 10)
            cv2.fillPoly(scoring_mask, [ellipse], WHITE)
            cell_to_score = cv2.bitwise_and(cell_to_score, scoring_mask)
            cv2.imwrite(out_path + str(cnt) + '.png', cell_to_score)

            cnt += 1
    return cnt


def merge_contours(too_small, area_per_pixel):
    """
    Merge contours that are close to each other

    :param too_small: List of candidate contours to be merged
    :param area_per_pixel: Area per pixel in the image
    :return: Merged contours
    """
    if len(too_small) < 2:
        return []
    centroids = []
    merged = []
    # Get centroids to compare distance
    for contour in too_small:
        moments = cv2.moments(contour)
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
        centroids.append([cx, cy])
    # Create array of flags to check if a contour has been merged with another
    already_merged = np.zeros(len(too_small), np.uint32)
    for i, centroid in enumerate(centroids[:-1]):
        if already_merged[i]:
            continue
        sq_dists = []
        # Get square distances to this contour for subsequent unmerged contours
        for j, centroid2 in enumerate(centroids[i + 1:]):
            if already_merged[i + j] != 0:
                continue
            sq_dist = (centroid[0] - centroid2[0]) * \
                      (centroid[0] - centroid2[0]) + \
                      (centroid[1] - centroid2[1]) * \
                      (centroid[1] - centroid2[1])
            sq_dists.append(sq_dist)
        # unmerged is a list of subsequent unmerged contours
        unmerged = [y for x, y in
                    zip(already_merged[i + 1:], too_small[i + 1:]) if x == 0]
        # closest_contours is a list of contours by distance from this one
        zipped = [x for x in zip(sq_dists, unmerged)]
        zipped.sort(key=lambda x: x[0])
        closest_contours = [x for _, x in zipped]
        contour = too_small[i]
        for j, contour2 in enumerate(closest_contours):
            new_contour = np.concatenate((contour, contour2))
            _, _, w, h = cv2.boundingRect(new_contour)
            area = w * h * area_per_pixel
            if area > 1.2 * MIN_AREA:
                break
            contour = new_contour
            already_merged[index_of_array(too_small, contour2)] = 1
        # Check area of completed contour. If it's still too small, ignore it
        _, _, w, h = cv2.boundingRect(contour)
        area = w * h * area_per_pixel
        if area >= 0.6 * MIN_AREA:
            merged.append(contour)

    return merged


def index_of_array(lst, target_arr):
    """
    Find the location of a list in another list

    :param lst: List containing sublists
    :param target_arr: List to locate
    :return: Index of target_arr in lst
    """
    for i, arr in enumerate(lst):
        if np.array_equal(arr, target_arr):
            return i
    raise ValueError


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Required arguments: path_to_img cell_dir distance_per_pixel",
              file=sys.stderr)
        exit(1)

    img = cv2.imread(sys.argv[1])
    if img is None:
        print("Image %s could not be read" % sys.argv[1],
              file=sys.stderr)
        exit(1)

    cell_dir = sys.argv[2]
    if not cell_dir[-1] == os.sep:
        cell_dir += os.sep
    utils.create_or_wipe_dir(cell_dir)

    dist_per_pixel = float(sys.argv[3])

    segment_region(img, cell_dir, 0, dist_per_pixel)
    print("Done segmenting")
