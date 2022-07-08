import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import glob
import os
import random
import argparse
import json
from preprocess import deform




def generator(text_dir,out_dir):
    """

    :param text_dir: directory containing the text files to be converted
    :param out_dir: output directory to save the images
    :return: None
    """


    text_files = glob.glob(text_dir+'/*.txt')
    imgs_out_dir = os.path.join(out_dir,'images')
    words_dict = dict()

    for text in text_files:
        f = open(text,'r')
        words=f.readline().strip().split(' ')
        for word in words:
            new_img = deform()
            FONT = random.choice(new_img.all_fonts())
            font = ImageFont.truetype(FONT,50)
            img = Image.new('RGBA',(500,100),(255,255,255))
            draw = ImageDraw.Draw(img)
            draw.text((0,10),word,fill=(0,0,0),font = font,language='hi')
            for i in range(4):
                img = new_img.add_deformity(img)
            img_loc = os.path.join(imgs_out_dir, f'{word}.png')
            words_dict[os.path.basename(img_loc)] = word
            img.save(img_loc)
        f.close()
    out_file = json.dumps(words_dict,ensure_ascii=False)
    out_file_path = os.path.join(out_dir,'labels.json')
    t = open(out_file_path,'w')
    t.write(out_file)
    t.close()


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('text_dir',help='directory containing the text files.',type = str)
    parser.add_argument('out_dir',help = 'output dir of the deformed images',type = str)
    args = parser.parse_args()

    generator(args.text_dir,args.out_dir)
