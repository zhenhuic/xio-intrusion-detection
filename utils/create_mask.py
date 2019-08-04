import numpy as np
import cv2


def line_params(p1, p2):
    """
    p:(x, y), y = w * x + b
    :param p1: point 1
    :param p2: point 2
    :return: w, b
    """
    x1, y1 = p1
    x2, y2 = p2

    w = (y2 - y1) / (x2 - x1)
    b = (y1 * x2 - x1 * y2) / (x2 - x1)

    return w, b


def y_(x, w, b):
    y = w * x + b
    return y


def x_(y, w, b):
    x = (y - b) / w
    return x


def create_mask(orig_img, lines):
    img = cv2.imread(orig_img)
    mask = np.zeros_like(img)
    height, width, channel = mask.shape
    print(height, width)

    left, top, right, bottom = lines
    for x in range(width):
        for y in range(height):
            if x_(y, left[0], left[1]) <= x <= x_(y, right[0], right[1]) and \
                    y_(x, top[0], top[1]) <= y <= y_(x, bottom[0], bottom[1]):
                mask[y, x, 2] = 255
    return mask


def main():
    orig_img = '../images/records/vlcsnap-2019-08-02-16h01m50s221.png'

    left = line_params((180, 210), (35, 370))
    top = line_params((180, 210), (500, 330))
    right = line_params((500, 330), (495, 479))
    bottom = line_params((0, 479), (495, 479))

    mask = create_mask(orig_img, [left, top, right, bottom])
    cv2.imshow('mask', mask)

    cv2.imwrite('../images/masks/xiazhewan.jpg', mask, )

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':

    img_path = '../images/records/vlcsnap-2019-08-02-16h01m50s221.png'
    mask_path = '../images/masks/xiazhewan.jpg'

    img = cv2.imread(img_path)
    mask = cv2.imread(mask_path)

    overlap = cv2.addWeighted(img, 1, mask, 0.6, 0)

    cv2.imshow('overlap', overlap)
    cv2.waitKey(0)

