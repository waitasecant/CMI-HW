# Turn PGM images into PNG images
from PIL import Image
import os

def convert_pgm_to_png(input_dir, output_dir):
    """Converts a PGM image file to a PNG image file."""
    try:
        cd = os.getcwd()
        input_dir = os.path.join(cd, input_dir)
        output_dir = os.path.join(cd, output_dir)

        print(f"Input Directory: {input_dir}")
        print(f"Output Directory: {output_dir}")
        pgm_files = []
        for root, _, files  in os.walk(input_dir):
            for file in files:
                if file.endswith(".pgm"):
                    pgm_files.append(os.path.join(root, file))
        c= 0
        for pgm_filepath in pgm_files:
            filename = os.path.basename(pgm_filepath)
            png_filename = os.path.splitext(filename)[0] + ".png"
            png_filepath = os.path.join(output_dir, png_filename)
            os.makedirs(output_dir, exist_ok=True)
            img = Image.open(pgm_filepath)
            img.save(png_filepath)        
            c+= 1
            print(f"Successfully converted {pgm_filepath} to {png_filepath}")
        print(f"Converted {c} PGM files to PNG format.")
    except FileNotFoundError:
        print(f"Error: PGM file not found at {input_dir}")
    except Exception as e:
        print(f"An error occurred: {e}")

pgm_dir = ""
png_dir = "faces"
convert_pgm_to_png(pgm_dir, png_dir)