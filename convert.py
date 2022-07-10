import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import glob
import os
import random
import argparse
import json
from tqdm import tqdm
import numpy as np
import cv2 as cv
import subprocess
from preprocess import deform
import shutil
from pathlib import Path


def generator(text_dir,out_dir):
    """

    :param text_dir: directory containing the text files to be converted
    :param out_dir: output directory to save the images
    :return: None
    """


    text_files = glob.glob(text_dir+'/*.txt')
    print(f'Files identified {text_files}')
    imgs_out_dir = os.path.join(out_dir,'images')
    words_dict = dict()

    counter = 1
    for text in tqdm(text_files):
        f = open(text,'r')
        words=f.readline().strip().split(' ')
        for word in tqdm(words):
            new_img = deform()
            FONT = random.choice(new_img.all_fonts())
            print(f'Font : {FONT}')
            FONTS_ADD = os.path.dirname(new_img.fonts[0])
            print(f'font add : {os.path.join(FONTS_ADD,FONT)}')
            # subprocess.run(f'cp {FONT_ADD} .')
            font_add = os.path.join(FONTS_ADD, FONT)
            font_dest = Path(FONT)
            shutil.copy(font_add, font_dest)
            font = ImageFont.truetype(FONT,50)
            img = Image.new('RGBA',(500,100),(255,255,255))
            draw = ImageDraw.Draw(img)
            draw.text((0,10),word,fill=(0,0,0),font = font)
            img = np.array(img)
            img = new_img.add_deformity(img)
            img_loc = os.path.join(imgs_out_dir, f'img_{counter}.png')
            words_dict[os.path.basename(img_loc)] = word
            cv.imwrite(img_loc,img)
            counter += 1
            # subprocess.run(f'rm {FONT}')
            os.remove(FONT)
        f.close()
    out_file = json.dumps(words_dict,ensure_ascii=False)
    out_file_path = os.path.join(out_dir,'labels.json')
    t = open(out_file_path,'w')
    t.write(out_file)
    t.close()


def dir(path):
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--text_dir',help='directory containing the text files.',type=dir)
    parser.add_argument('--out_dir',help = 'output dir of the deformed images',type=dir)
    args = parser.parse_args()
    print(f'Text directory : {args.text_dir}, Output directory : {args.out_dir}')

    generator(args.text_dir,args.out_dir)

if __name__ == '__main__':
    args()
