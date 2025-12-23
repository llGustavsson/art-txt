from base_converter import BaseConverter
from typing import cast, Sequence

#Chars that will be used
CHARS = "@%#*+=-:. "

class AsciiConverter(BaseConverter):
    def __init__(
                    self, 
                    image_path: str, 
                    width: int = 100, 
                    invert: bool = False, 
                    aspect_ratio_correction: float = 0.5
                 ) -> None:
        
        super().__init__(image_path, width, invert, aspect_ratio_correction)

    # Converter pixels in gray chars
    def gray_converter(self) -> str:
        gray_pixels = cast(Sequence[int], self.gray_image.getdata())
        scale = len(CHARS)
        chars = []
        
        for pixel in gray_pixels:
            base_char = CHARS[pixel * scale // 256]
            chars.append(base_char)

        return self._group_into_lines(chars, self.gray_image.width)

    # Converter pixels in rgb chars
    def rgb_converter(self) -> str:
        gray_pixels = cast(Sequence[int], self.gray_image.getdata())
        rgb_pixels =cast(Sequence[tuple[int, int, int]], self.rgb_image.getdata())
        
        scale = len(CHARS)
        chars = []

        for i, pixel in enumerate(gray_pixels):
            base_char = CHARS[pixel * scale // 256]
            rgb_chars = self.colorize(base_char, rgb_pixels[i])
            chars.append(rgb_chars)

        return self._group_into_lines(chars, self.rgb_image.width)
    
    # slice list of chars into rows
    def _group_into_lines(self, chars: list[str], width: int) -> str:
        lines = ["".join(chars[i:i + width]) for i in range(0, len(chars), width)]

        return "\n".join(lines)