import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import random
from preprocess import deform




def main():

    name=random.choice(glob.glob('/content/content/sanskrit/*.txt'))
    f = open(name,'r')
    word=f.readline().strip().split(' ')[0]
    print(word)





    new_img = deform(img)
    FONT = random.choice(new_img.all_fonts())
    # FONTS = new_img.fonts(NUM_OF_FONTS)

    font = ImageFont.truetype(FONT,50)
    img = Image.new('RGBA',(500,100),(255,255,255))
    draw = ImageDraw.Draw(img)
    draw.text((0,10),'',fill=(0,0,0),font = font,language='hi')
    for i in range(4):
        im = new_img.add_deformity()

    img.save('aadharshila.png')