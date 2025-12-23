from PIL import Image, ImageOps,ImageEnhance

class BaseConverter:
    def __init__(
                    self, 
                    image_path: str, 
                    width: int = 100, 
                    invert: bool = False, 
                    aspect_ratio_correction: float = 0.5
                 ) -> None:
    
        self.image_path = image_path
        self.width = width
        self.invert = invert
        self.aspect_ratio_correction = aspect_ratio_correction

        self.original_image = self._image_load()
        self.gray_image = self._prepare_gray()
        self.rgb_image = self._prepare_rgb()

    # Process to return gray image
    def _prepare_gray(self):
        image = self.original_image
        image_enhanced = self._image_enhance(image)

        if self.invert:
            image_enhanced = self._invert(image_enhanced)

        image_resized = self._resize_image(image_enhanced)
        gray_image = image_resized.convert("L")

        return gray_image
    
    # Process to return rgb image
    def _prepare_rgb(self):
        image = self.original_image
        image_enhanced = self._image_enhance(image)

        image_resized = self._resize_image(image_enhanced)
        image_rgb = image_resized

        return image_rgb
    
    # Load the image and use .convert to assure RGB color channels
    def _image_load(self) -> Image.Image:
        try:
            image = Image.open(self.image_path).convert("RGB")
            return image
        except Exception as e:
            raise RuntimeError(f"Failed to load the image: {e}")

    # Apply filters on the image to make it look better
    def _image_enhance(self, image: Image.Image) -> Image.Image:
        image_brightness = ImageEnhance.Brightness(image).enhance(1.10)
        image_saturation = ImageEnhance.Color(image_brightness).enhance(1.10)
        image_contrast = ImageEnhance.Contrast(image_saturation).enhance(1.25)
        image_sharpness = ImageEnhance.Sharpness(image_contrast).enhance(1.15)

        # Apply gamma
        gamma = 1.1
        lut = [pow(x / 255.0, gamma) * 255 for x in range(256)]
        image_gamma = image_sharpness.point(lut * 3)

        image_dither = image_gamma.quantize(
                                                colors=256, 
                                                method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG
                                            )
        
        image_enhanced = image_dither.convert("RGB")
        return image_enhanced
    
    # Resize image to respect ascii and braille
    def _resize_image(self, image: Image.Image) -> Image.Image:
        width_ratio = self.width / float(image.size[0])
        new_height = int(float(image.size[1] * width_ratio * self.aspect_ratio_correction))
        resized_image = image.resize((self.width, new_height))

        return resized_image

    # Invert the grayscale
    def _invert(self, image: Image.Image) -> Image.Image:
        image_inverted = ImageOps.invert(image)
        return image_inverted

    # Apply color to chars
    @staticmethod
    def colorize(char: str, rgb: tuple[int, int, int]) -> str:
        r, g, b = rgb

        return f"\x1b[38;2;{r};{g};{b}m{char}\x1b[0m"