from .ascii_converter import AsciiConverter
from .braille_converter import BrailleConverter
from .cli_tool import ArgParser

def main():
    args = ArgParser().parse()

    # Take parameters
    ascii_converter = AsciiConverter(
                                        image_path=args.image, 
                                        width=args.size, 
                                        invert=args.invert
                                     )
    
    braille_converter = BrailleConverter(
                                            image_path=args.image, 
                                            width=args.size, 
                                            invert=args.invert
                                         )

    # Save and print the art
    match args.type:
        case "ascii":
            ascii_gray_art = ascii_converter.gray_converter()
            ascii_rgb_art = ascii_converter.rgb_converter()

            with open(args.ascii_gray, "w", encoding="utf-8") as f:
                f.write(ascii_gray_art)
            with open(args.ascii_rgb, "w", encoding="utf-8") as f:
                f.write(ascii_rgb_art)

            print("\n##### ASCII GRAY ART #####\n")
            print(ascii_gray_art)

            print("\n##### ASCII RGB ART #####\n")
            print(ascii_rgb_art)

        case "braille":
            braille_gray_art = braille_converter.gray_converter()
            braille_rgb_art = braille_converter.rgb_converter()
            
            with open(args.braille_gray, "w", encoding="utf-8") as f:
                f.write(braille_gray_art)
            with open(args.braille_rgb, "w", encoding="utf-8") as f:
                f.write(braille_rgb_art)

            print("\n##### Braille GRAY ART #####\n")
            print(braille_gray_art)

            print("\n##### Braille RGB ART #####\n")
            print(braille_rgb_art)

if __name__ == "__main__":
    main()