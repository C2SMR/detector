import sys

import cv2
import time


def main():
    time_start = time.time()
    image = cv2.imread(sys.argv[1])
    image = cv2.convertScaleAbs(image, alpha=1.4, beta=0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, filter = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    filter = cv2.bitwise_not(filter)

    nb_line_max_pixel = 0
    nb_max_pixel = 0
    width_picture = filter.shape[1]
    height_picture = filter.shape[0]
    for i in range(height_picture - 50):
        nb_pixel = 0
        for j in range(width_picture):
            if filter[i][j] == 255:
                nb_pixel += 1
        if nb_pixel > nb_max_pixel:
            nb_line_max_pixel = i
            nb_max_pixel = nb_pixel

    cv2.line(image, (0, nb_line_max_pixel),
             (width_picture, nb_line_max_pixel),
             (0, 255, 0), 2)

    for i in range(nb_line_max_pixel):
        for j in range(width_picture):
            if filter[i][j] == 255:
                print(f'x: {j} y: {i}')

    print(nb_line_max_pixel)
    print(nb_max_pixel)
    print(time.time() - time_start)

    while True:

        image = cv2.resize(image, (800, 600))
        filter = cv2.resize(filter, (800, 600))
        cv2.imshow('thresh', filter)
        cv2.imshow('image', image)

        if cv2.waitKey(30) == 'q':
            break


if __name__ == "__main__":
    main()
