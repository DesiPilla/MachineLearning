from PIL import Image

def getPixels(filename):
    image = Image.open(filename).rotate(270)
    pixels = list(image.getdata())
    image.show()
    image.close()
    return pixels
    
image1 = getPixels('spencer.jpg')
image2 = getPixels('green.jpg')
image3 = getPixels('dupont.jpg')