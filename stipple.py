from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("image", help="set image to polarize")
args = parser.parse_args()

image = args.image

im = Image.open(image)
im.load()
im = im.convert('1')
im.save('dither.pbm')
