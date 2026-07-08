import sys

from PIL import Image
from rembg import remove


def process_image(input_path, output_path):
    try:
        print(f"Loading image from {input_path}")
        input_image = Image.open(input_path)
        print("Removing background...")
        # Alpha matting for cleaner edges
        output_image = remove(input_image, alpha_matting=True)
        print(f"Saving to {output_path}")
        output_image.save(output_path)
        print("Done!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python remove_bg.py <input> <output>")
        sys.exit(1)
    process_image(sys.argv[1], sys.argv[2])
