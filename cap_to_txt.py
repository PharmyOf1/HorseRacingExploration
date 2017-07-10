import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

im = Image.open("/home/una0464/projects/horseracing/captcha.jpg") # the second one
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(100)
im = im.convert('1')
im.save('captcha2.jpg')
text = pytesseract.image_to_string(Image.open('captcha2.jpg'))
print(text)
