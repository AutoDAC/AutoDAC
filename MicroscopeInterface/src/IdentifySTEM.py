import os
import shutil
import cv2
import numpy as np
import operator

from MicroscopeInterface.src.LeicaMicroscope         import LeicaMicroscope
from MicroscopeInterface.src.LeicaUI                 import LeicaUI
from MicroscopeInterface.src.Buttons.LeftButton      import LeftButton
from MicroscopeInterface.src.Buttons.RightButton     import RightButton
from MicroscopeInterface.src.Buttons.ForwardsButton  import ForwardsButton
from MicroscopeInterface.src.Buttons.BackwardsButton import BackwardsButton
from MicroscopeInterface.src.Buttons.CaptureImage    import CaptureImage
from MicroscopeInterface.src.Buttons.MakeLive        import MakeLive
from MicroscopeInterface.src.Buttons.AcquisitionTab  import AcquisitionTab
from MicroscopeInterface.src.Buttons.ExperimentsTab  import ExperimentsTab
from MicroscopeInterface.src.Buttons.SeqButton       import SeqButton
from MicroscopeInterface.src.Buttons.StartButton     import StartButton
from MicroscopeInterface.src.Buttons.SaveButton      import SaveButton
from MicroscopeInterface.src.LifParser               import extract_merged_images

import ImageProcessing.src.analyse as analyse


def get_abs_path(rel_path):
    """
    Take path relative from program run location and convert to absolute path

    :param rel_path: Relative path
    :return: Absolute path
    """
    return os.path.join(os.getcwd(), rel_path)


def setup_microscope(experiment_path, save_path):
    """
    Setup microscope object

    :param experiment_path: Path to LAS generated .lif file
    :param save_path: Path to save analysis result
    :return: Microscope object
    """
    # Make buttons
    import pyautogui
    lb = LeftButton(image=get_abs_path('MicroscopeInterface/src/images/move_left.png'),           gui_interface=pyautogui)
    rb = RightButton(image=get_abs_path('MicroscopeInterface/src/images/move_right.png'),         gui_interface=pyautogui)
    fb = ForwardsButton(image=get_abs_path('MicroscopeInterface/src/images/move_forwards.png'),   gui_interface=pyautogui)
    bb = BackwardsButton(image=get_abs_path('MicroscopeInterface/src/images/move_backwards.png'), gui_interface=pyautogui)
    ci = CaptureImage(image=get_abs_path('MicroscopeInterface/src/images/capture_image.png'),     gui_interface=pyautogui)
    ml = MakeLive(image=get_abs_path('MicroscopeInterface/src/images/make_live.png'),             gui_interface=pyautogui)
    aq = AcquisitionTab(image=get_abs_path('MicroscopeInterface/src/images/acquisition_tab.png'), gui_interface=pyautogui)
    ex = ExperimentsTab(image=get_abs_path('MicroscopeInterface/src/images/experiments_tab.png'), gui_interface=pyautogui)
    se = SeqButton(image=get_abs_path('MicroscopeInterface/src/images/seq_button.png'),           gui_interface=pyautogui)
    st = StartButton(image=get_abs_path('MicroscopeInterface/src/images/start_button.png'),       gui_interface=pyautogui)
    sv = SaveButton(image=get_abs_path('MicroscopeInterface/src/images/Save.png'),                gui_interface=pyautogui)

    # Compose UI
    ui = LeicaUI(fb, bb, lb, rb, ci, ml, aq, ex, se, st, sv)

    # Compose microscope
    return LeicaMicroscope(ui, experiment_path)


def identify_stem(microscope):
    """
    Scan tissue and take pictures of STEM cells

    :param microscope: used to take pictures
    :return: None
    """
    # Clean working_dir to begin
    clean_working_dir(microscope)

    # Take a tile scan at multiple  z-planes
    microscope.tile_scan()

    # Take pictures will populate the microscope.working_dir
    metadata = lif_to_tif(microscope=microscope)

    dist_per_pixel = get_first_image(metadata)

    # Merge z-stacks
    merged_image = merge_z_stack(microscope=microscope)

    # Find cell regions
    cell_regions = find_cells(merged_image, dist_per_pixel)

    for i in range(0, len(cell_regions)):
        # Find brightest z-stack for each cell
        brightest_z_plane = analyse_z_stack(microscope, cell_regions[i])
        cv2.imwrite(microscope.result_dir + "/" + str(i) + ".tif", brightest_z_plane)

    # Score images in working directory
    score = analyse.analyse_dir(microscope.result_dir + os.sep, dist_per_pixel)
    return score

def lif_to_tif(microscope):
    """
    Take picture with microscope and then do the .lif to .tif conversion and place all of these in the microscope.working_dir

    :param microscope: microscope to take picture with
    :return {path: (physicalsizex, ...)} image metadata
    """
    metadata = extract_merged_images(microscope.experiment_path, microscope.working_dir)

    image_files = metadata.keys()

    for i in image_files:
        image = cv2.imread(i)
        image += 50
        microscope.rgb_images.append(image)

    return metadata

def merge_z_stack(microscope):
    """
    Squash all z-stacks into one image

    :param microscope: microscope object contains rgb-images to squash
    :return squashed_image
    """
    squashed_image = np.zeros(microscope.rgb_images[0].shape, np.uint8)

    for image in microscope.rgb_images:
        squashed_image = cv2.add(squashed_image, image)

    return squashed_image

def analyse_z_stack(microscope, region):
    """
    Analyse z-stacks to find best image

    :param microscope: microscope to take picture with
    :param region: the region in each z-stack we're looking at
    :return region of best image we could find, using the z-stack
    """
    x_s, x_e, y_s, y_e = region
    z_images = microscope.rgb_images
    z_score = []

    for i in range(0, len(z_images)):
        image_region = z_images[i][y_s:y_e, x_s:x_e, :]
        # Set threshold to 30 - arbitrary choice
        z_score.append(calculate_brightest_green(image_region, 30))

    max_index, _ = max(enumerate(z_score), key=operator.itemgetter(1))
    return z_images[max_index][y_s:y_e, x_s:x_e, :]

def find_cells(image, dist_per_pixel):
    """
    Look at image and locate cells

    :param image: pixel matrix
    :return: array of (startx, starty, endx, endy) regions
    """
    return segment_region(image, dist_per_pixel)

def segment_region(img, dist_per_pixel):
    """
    Find regions containing cells in the image

    :param img: Image object
    :param dist_per_pixel: How big wide each pixel is
    :return: List of regions
    """
    BR_DEF = 21
    NT_MIN = 14
    MIN_AREA = 2500
    MAX_AREA = 3600
    WHITE = (255, 255, 255)

    result = []
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

        xs = max(0, x-10)
        xe = min(x+w+10, img_w)
        ys = max(y-10, 0)
        ye = min(y+h+10, img_h)
        result.append((xs, xe, ys, ye))
    return result

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

def get_first_image(images):
    """
    Dict of images, return first one

    :param images: dictionary of images
    :return: first image value
    """
    for i in images:
        return images[i]


def calculate_brightest_green(image, threshold):
    """
    Calculate total of all green pixel intensities

    :param image:
    :param threshold: values to threshold to zero
    :return: intensity total
    """
    _, green, _ = cv2.split(image)
    _, filtered_green = cv2.threshold(green, threshold, 0, cv2.THRESH_TOZERO)
    return np.sum(filtered_green, dtype=np.uint32)


def clean_working_dir(microscope):
    """
    Delete all images from the microscope.working_dir and move the brightest one to the microscope.result_dir

    :param brightest_image:
    :param microscope:
    :return: None
    """
    shutil.rmtree(microscope.working_dir)
    microscope.working_dir = microscope.generate_dir("working_dir")
