from .base_converter import BaseConverter

DOT_POSITIONS = [
                    (0, 0), (0, 1), (0, 2), (1, 0), 
                    (1, 1), (1, 2), (0, 3), (1, 3)
                ]

class BrailleConverter(BaseConverter):
    def __init__(
                    self, 
                    image_path: str, 
                    width: int = 100, 
                    invert: bool = False
                 ) -> None:
        
        super().__init__(image_path, width=width * 2, invert=invert, aspect_ratio_correction=1.0)

    # Convert image into braille blocks
    def gray_converter(self) -> str:
        width, height = self.gray_image.size
        pixels = self.gray_image.load()
        lines = []

        # Loop through the image in 2×4 pixel blocks
        for y in range(0, height - (height % 4), 4):
            row_char = []
            for x in range(0, width - (width % 2), 2):
                # Gather the 8-pixel block
                block = []
                for dx, dy in DOT_POSITIONS:
                    px = x + dx
                    py = y + dy

                    if px < width and py < height:
                        value = pixels[px, py] # type: ignore
                        block.append(value)
                
                # Decide how many dots to turn on
                avg = sum(block) / len(block)
                dots_on = int((255 - avg) / 32)

                # Pick which dots to activate and compute the braille unicode
                indices = sorted(range(len(block)), key=lambda i: block[i])[:dots_on]
                cell_value = sum(1 << i for i in indices)
                dots = chr(0x2800 + cell_value)

                row_char.append(dots)

            lines.append("".join(row_char))

        return "\n".join(lines)

    # Convert image into a rgb braille blocks
    def rgb_converter(self):
        width, height = self.rgb_image.size
        rgb_pixel = self.rgb_image.load()
        gray_pixel = self.gray_image.load()
        lines = []

        # Loop through the image in 2×4 pixel blocks
        for y in range(0, height - (height % 4), 4):
            row_char =[]
            for x in range(0, width - (width % 2), 2):
                # Gather the 8-pixel block
                gray_block = []
                rgb_block = []

                for dx, dy in DOT_POSITIONS:
                    px = x + dx
                    py = y + dy

                    if px < width and py < height:
                        gray_block.append(gray_pixel[px, py]) # type: ignore
                        rgb_block.append(rgb_pixel[px, py])# type: ignore

                # Decide how many dots to turn on
                avg_gray = sum(gray_block) / len(gray_block)
                dots_on = int((255 - avg_gray) / 32)
                
                # Pick which dots to activate and compute the braille unicode with colors
                indices = sorted(range(len(gray_block)), key=lambda i: gray_block[i])[:dots_on]

                cell_value = sum(1 << i for i in indices)
                dots = chr(0x2800 + cell_value)

                avg_rgb =self._avg_color(rgb_block)
                
                colorized = self.colorize(dots, avg_rgb)

                row_char.append(colorized)

            lines.append("".join(row_char))

        return "\n".join(lines)

    # Average of all rgb tuples in the block        
    def _avg_color(self, rgb_block):
        n = len(rgb_block)
        if n == 0:
            return(255, 255, 255)
        
        r = sum(c[0] for c in rgb_block) // n
        g = sum(c[1] for c in rgb_block) // n
        b = sum(c[2] for c in rgb_block) // n

        return(r, g, b)