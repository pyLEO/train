"""
this module solve image crop
"""


from PIL import Image
from io import BytesIO

def crop_image(img):
    im = Image.open(BytesIO(img))
    im = im.crop((left, top, right, bottom))
    im.save(r'C:\b.png')



