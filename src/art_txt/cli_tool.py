import argparse
import os

class ArgParser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(prog="art-txt", description="Convert an image into Ascii or Braille art")

        self.setup_arguments()

    def setup_arguments(self):
        # Image path
        self.parser.add_argument("image", type=str, help="Image file path")
        # Art type
        self.parser.add_argument(
                                    "-t", "--type", 
                                    choices=["ascii", "braille"], 
                                    default="ascii", 
                                    help="Choose between ASCII or braille art type (default: ascii)"
                                 )
        # Size in chars
        self.parser.add_argument(
                                    "--size", 
                                    type=int, 
                                    default=100, 
                                    help="Art width (default : 100)"
                                 )
        # Invert image grayscale
        self.parser.add_argument(
                                    "--invert", 
                                    action="store_true",  
                                    help="Invert image grayscale"
                                 )
        
    def parse(self):
        args = self.parser.parse_args()

        # Save image in a default folder and file name
        image_name = os.path.splitext(os.path.basename(args.image))[0]
        home = os.path.expanduser("~")
        result_folder = os.path.join(home, "arts_results")
        os.makedirs(result_folder, exist_ok=True)

        args.ascii_gray = os.path.join(result_folder, f"{image_name}_ascii_gray.txt")
        args.ascii_rgb = os.path.join(result_folder, f"{image_name}_ascii_rgb.txt")

        args.braille_gray = os.path.join(result_folder, f"{image_name}_dots_gray.txt")
        args.braille_rgb = os.path.join(result_folder, f"{image_name}_dots_rgb.txt")

        return args