from PIL import Image, ImageOps

def convert_to_grayscale(img):
    path = img if isinstance(img, str) else img.path
    print path
    im = Image.open(path)
    im = ImageOps.grayscale(im)
    im.save(path)
