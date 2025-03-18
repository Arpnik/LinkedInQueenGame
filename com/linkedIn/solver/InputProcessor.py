import cv2
import numpy as np
from sklearn.cluster import KMeans
import math
from com.linkedIn.solver.Grid import Node, Grid


class InputProcessor:
    def __init__(self, img_path):
        self.img_path = img_path
        pass

    def extract_grid_colors(self):
        # Read the image
        img = cv2.imread(self.img_path)
        if img is None:
            raise ValueError("Could not read the image. Please check the image path.")

        # Convert to RGB (from BGR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Get image dimensions
        height, width = img.shape[:2]

        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding to handle varying lighting
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)

        # Add morphological operations to clean up the image
        kernel = np.ones((3, 3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        # Find contours using RETR_TREE to get all cells
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Filter and sort contours
        cells = []
        colors = set()

        avg_area = np.mean([cv2.contourArea(cnt) for cnt in contours])

        for contour in contours:
            area = cv2.contourArea(contour)
            # Filter contours by area (should be close to average cell area)
            if area > avg_area * 0.5 and area < avg_area * 2:
                x, y, w, h = cv2.boundingRect(contour)
                # Filter out very small or very large rectangles
                if w > width * 0.05 and h > height * 0.05 and w < width * 0.3 and h < height * 0.3:
                    cells.append((x, y, w, h))

        # Detect grid dimensions
        unique_y = sorted(list(set([y for x, y, w, h in cells])))
        row_height = np.mean(np.diff(unique_y))
        num_rows = len(unique_y)

        # Sort cells by position
        cells.sort(key=lambda x: (round(x[1] / row_height), x[0]))

        # Initialize grid structure
        grid = []
        row = []
        current_grid = Grid(math.isqrt(len(cells)))
        current_row = 0
        cur_col = 0
        cur_r = 0

        # Extract dominant color for each cell
        for x, y, w, h in cells:
            # Check if we're on a new row
            cell_row = round(y / row_height)
            if cell_row > current_row:
                if row:
                    grid.append(row)
                    cur_col = 0
                    cur_r += 1
                row = []
                current_row = cell_row

            # Get cell region with padding to avoid border
            padding = 5
            cell_img = img_rgb[y + padding:y + h - padding, x + padding:x + w - padding]

            # Reshape the cell image for K-means
            pixels = cell_img.reshape(-1, 3)

            # Apply K-means clustering to find dominant color
            kmeans = KMeans(n_clusters=1, n_init=10)
            kmeans.fit(pixels)
            dominant_color = kmeans.cluster_centers_[0].astype(int)

            # Convert RGB values to hex color code
            hex_color = '#{:02x}{:02x}{:02x}'.format(*dominant_color)

            colors.add(hex_color)
            # node = Node(hex_color)
            # # print(cur_r, cur_col)
            # # current_grid.grid[cur_r, cur_col] = node
            current_grid.addNode(cur_r, cur_col, hex_color)
            cur_col += 1

            row.append({
                'position': (x, y),
                'size': (w, h),
                'color': hex_color,
                'rgb': tuple(dominant_color)
            })

        # Append the last row
        if row:
            grid.append(row)
            cur_col = 0
            cur_r += 1

        return grid, current_grid

    def visualize_grid(image_path, grid):
        """Visualize the detected grid cells on the image"""
        img = cv2.imread(image_path)

        for row in grid:
            for cell in row:
                x, y = cell['position']
                w, h = cell['size']
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Detected Grid', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
