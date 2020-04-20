import cv2
import numpy as np


def resize(image: np.ndarray, width: int = None, height: int = None, inter: int = cv2.INTER_AREA) -> np.ndarray:
    """
    Resize image proportionally

    :param image: image to resize
    :param width: new width
    :param height: new height
    :param inter: interpolation method
    :return: resized image
    """
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        ratio = height / float(h)
        dim = (int(w * ratio), height)
    else:
        ratio = width / float(w)
        dim = (width, int(h * ratio))
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized
