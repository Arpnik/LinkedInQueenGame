import cv2
import numpy as np

class OutputProcessor:
    def __init__(self, board):
        self.board = board
        self.cell_size = 80 
        self.margin = 40
        self.queen_image = None
        self.load_queen_image()
        self.draw_grid()

    def load_queen_image(self):
        """Load and resize queen image, or create a text-based queen if image not found"""
        try:
            self.queen_image = cv2.imread("./resources/queen.png", cv2.IMREAD_UNCHANGED)
            if self.queen_image is not None:
                self.queen_image = cv2.resize(self.queen_image, (self.cell_size - 20, self.cell_size - 20))
        except:
            self.queen_image = None

    def hex_to_bgr(self, hex_color):
        """Convert hex color to BGR format"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (rgb[2], rgb[1], rgb[0])  # Convert to BGR

    def draw_grid(self):
        """Draw the chess board with colors and queens"""
        # Calculate board dimensions
        board_size = self.board.size
        width = board_size * self.cell_size + 2 * self.margin
        height = board_size * self.cell_size + 2 * self.margin

        # Create blank image
        image = np.ones((height, width, 3), dtype=np.uint8) * 255

        # Draw cells
        for row in range(board_size):
            for col in range(board_size):
                # Calculate cell coordinates
                x1 = col * self.cell_size + self.margin
                y1 = row * self.cell_size + self.margin
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Get cell color and convert to BGR
                cell = self.board.grid[row][col]
                color = cell.color if cell.color.startswith('#') else f"#{cell.color}"
                bgr_color = self.hex_to_bgr(color)

                # Draw colored cell
                cv2.rectangle(image, (x1, y1), (x2, y2), bgr_color, -1)
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 0), 1)  # Border

                # Draw queen if present
                if cell.isQueenPlaced:
                    if self.queen_image is not None:
                        # Calculate position to center the queen image
                        queen_y = y1 + 10
                        queen_x = x1 + 10
                        
                        # Get alpha channel if available
                        if self.queen_image.shape[2] == 4:
                            # Image has alpha channel
                            alpha = self.queen_image[:, :, 3] / 255.0
                            for c in range(3):
                                image[queen_y:queen_y + self.queen_image.shape[0],
                                      queen_x:queen_x + self.queen_image.shape[1], c] = \
                                    image[queen_y:queen_y + self.queen_image.shape[0],
                                          queen_x:queen_x + self.queen_image.shape[1], c] * (1 - alpha) + \
                                    self.queen_image[:, :, c] * alpha
                        else:
                            # No alpha channel, just overlay the image
                            image[queen_y:queen_y + self.queen_image.shape[0],
                                  queen_x:queen_x + self.queen_image.shape[1]] = self.queen_image
                    else:
                        # Draw 'Q' if no image available
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        text_size = cv2.getTextSize('Q', font, 1, 2)[0]
                        text_x = x1 + (self.cell_size - text_size[0]) // 2
                        text_y = y1 + (self.cell_size + text_size[1]) // 2
                        cv2.putText(image, 'Q', (text_x, text_y), font, 1, (0, 0, 0), 2)

        # Add row and column labels
        font = cv2.FONT_HERSHEY_SIMPLEX
        for i in range(board_size):
            # Column labels (A, B, C, ...)
            label = chr(65 + i)
            cv2.putText(image, label, 
                       (self.margin + i * self.cell_size + self.cell_size//3, self.margin//2),
                       font, 0.5, (0, 0, 0), 1)
            
            # Row labels (1, 2, 3, ...)
            label = str(i + 1)
            cv2.putText(image, label,
                       (self.margin//3, self.margin + i * self.cell_size + self.cell_size//2),
                       font, 0.5, (0, 0, 0), 1)

        # Display the image
        cv2.imshow('LinkedIn Queen Game', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()