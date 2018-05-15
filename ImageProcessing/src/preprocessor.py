# Module for performing a Gaussian Blur, noise removal, Canny edge detection
# and closure on an image.
import numpy as np
import cv2

BR_DEF = 21
NT_MIN = 14
CTL_DEF = 20
CTH_DEF = 108
KNL_DEF = np.ones((3, 3), np.uint8)


def prepare(img, blur_radius=BR_DEF, noise_thresh=NT_MIN): 
    """
    perform Gaussian blur and threshold the image to remove noisy pixels

    :param img: image to be prepared 
    :param blur_radius: size of blur radius
    :param noise_thresh: threshold on which to reject pixesls

    :return: prepared image is returned
    """
    check_params(img, blur_radius)

    # Blur the image to smooth out the cell images
    blurred = cv2.GaussianBlur(img, (blur_radius, blur_radius), 0)
    # cv2.imwrite('img/blurred.png', blurred)

    # Apply a threshold to remove background noise
    _, threshold = cv2.threshold(blurred, noise_thresh, 255, cv2.THRESH_BINARY)
    # cv2.imwrite('img/thresh.png', threshold)

    if len(img.shape) == 3:
        threshold = cv2.cvtColor(threshold, cv2.COLOR_BGR2GRAY)

    return threshold


# Separate function to not clutter the prepare function
def check_params(img, blur_radius):
    """
    Checks parameters passed in to prepare function

    :param img: image passed into prepare function
    :param blur_radius: blur radius passed into prepare function

    :return: throws exception if any of the parmeters are invalid
    """
    if not hasattr(img, 'ndim'):
        raise TypeError('Images should be numpy arrays')
    if img.ndim < 2 or img.ndim > 3:
        raise TypeError('Images should be multidimensional numpy arrays. First'
                        'two dimensions are pixel coordinates. Grayscale images'
                        'have a single value at these coordinates, colour'
                        'images have another list containing BGR(A) values.')

    if len(img.shape) == 3:
        if not img.shape[2] == 3:
            raise TypeError('Images should be one or three channels only.')

    try:
        if blur_radius % 2 != 1 or blur_radius < 0:
            raise ValueError('Blur radius must be odd')
    except TypeError:
        raise TypeError('Blur Radius must be a number')
