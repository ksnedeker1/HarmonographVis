from PyQt5.QtGui import QImage, QColor
import numpy as np

import time

class ImageBlender:
    """Blends images and creates the image of the harmonograph."""
    def __init__(self, width: int, height: int, min_alpha: int = 25, steps: int = 10):
        """Initializes the image blender."""
        self.width = width
        self.height = height
        self.min_alpha = min_alpha
        self.alpha_increment = (255 - min_alpha) / steps

        self.reset()

    def reset(self):
        """Resets the image, the draw object, the intensities, and the set of crossed pixels."""
        self.intensities = np.zeros((self.width, self.height), dtype=np.float64)
        self.crossed_pixels = np.zeros((self.width, self.height), dtype=bool)
        self.image = QImage(self.width, self.height, QImage.Format_RGB32)

    def blend(self, x: np.ndarray[int], y: np.ndarray[int]) -> QImage:
        """Blends the image based on the given x and y coordinates."""
        xi_prev, yi_prev = int(x[0]), int(y[0])
        for i in range(1, len(x)):
            xi, yi = int(x[i]), int(y[i])

            # Exclude last point in line to avoid repetition as it marks the beginning of the following line
            for px, py in list(self.bresenham(xi_prev, yi_prev, xi, yi))[:-1]:
                # px, py = min(px, self.width - 1), min(py, self.height - 1)  # Ensure the coordinates are within the array bounds

                if not self.crossed_pixels[px, py]:
                    self.intensities[px, py] = self.min_alpha
                    self.crossed_pixels[px, py] = True
                else:
                    self.intensities[px, py] = min(255, self.intensities[px, py] + self.alpha_increment)

            xi_prev, yi_prev = xi, yi

        # Convert intensities array to QImage
        img_array_uint8 = self.intensities.astype(np.uint8).copy()  # copy the array and convert it to uint8 type
        img_array_qcolor = np.stack([img_array_uint8] * 3,
                                    axis=-1)  # repeat array 3 times along a new axis to create RGB image
        height, width = img_array_qcolor.shape[:2]
        bytes_per_line = 3 * width  # number of bytes in a line (3 bytes per pixel for RGB)

        # Create QImage from the numpy array
        self.image = QImage(img_array_qcolor.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return self.image

    @staticmethod
    def bresenham(x0: int, y0: int, x1: int, y1: int):
        """Generates points on a line using Bresenham's line algorithm."""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1

        if dx > dy:
            err = dx / 2.0
            while x != x1:
                yield x, y
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                yield x, y
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        yield x, y