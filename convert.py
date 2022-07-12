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
from preprocess import deform
import shutil
from pathlib import Path


def create_dataset(train: bool,out_dir,text_files):
    """

    :param train: whether to create train or val dataset
    :param out_dir: the main output directory containing train and val sub folders
    :param text_files: the list of text files 
    :return:
    """

    words_dict = dict()
    counter = 1
    if train:
      if not os.path.isdir(f"{out_dir}/train"):
        os.mkdir(f"{out_dir}/train")
      train_path = os.path.join(out_dir,'train')
      if not os.path.isdir(f"{train_path}/images"):
        os.mkdir(f"{train_path}/images")
      imgs_out_dir = os.path.join(train_path,'images')
      a = 0
      b = int(len(text_files)*0.7)
    else:
      if not os.path.isdir(f"{out_dir}/val"):
        os.mkdir(f"{out_dir}/val")
      val_path = os.path.join(out_dir,'val')
      if not os.path.isdir(f"{val_path}/images"):
        os.mkdir(f"{val_path}/images")
      imgs_out_dir = os.path.join(val_path,'images')
      a = int(len(text_files)*0.7)
      b = len(text_files)


    for text in tqdm(text_files[a:b]):
        f = open(text,'r')
        words=f.readline().strip().split(' ')
        for word in tqdm(words):
            new_img = deform()
            FONT = random.choice(new_img.all_fonts())
            # print(f'Font : {FONT}')
            FONTS_ADD = os.path.dirname(new_img.fonts[0])
            # print(f'font add : {os.path.join(FONTS_ADD,FONT)}')
            # subprocess.run(f'cp {FONT_ADD} .')
            font_add = os.path.join(FONTS_ADD, FONT)
            font_dest = Path(FONT)
            shutil.copy(font_add, font_dest)
            font = ImageFont.truetype(FONT,50)
            img = Image.new('RGBA',(1000,100),(255,255,255))
            draw = ImageDraw.Draw(img)
            draw.text((0,10),word,fill=(0,0,0),font = font)
            img = np.array(img)
            img = new_img.add_deformity(img)
            img_loc = os.path.join(imgs_out_dir, f'img_{counter}.png')
            words_dict[os.path.basename(img_loc)] = word
            cv.imwrite(img_loc,img)
            counter += 1
            print(counter)
            os.remove(FONT)
        f.close()
    out_file = json.dumps(words_dict,ensure_ascii=False)
    if train:
        out_file_path = os.path.join(train_path,'labels.json')
    else:
        out_file_path = os.path.join(val_path,'labels.json')
    t = open(out_file_path,'w')
    t.write(out_file)
    t.close()

def generator(text_dir,out_dir):
    """

    :param text_dir: directory containing the text files to be converted
    :param out_dir: output directory to save the images
    :return: None
    """


    text_files = glob.glob(text_dir+'/*.txt')
    print(f'Files identified {text_files}')
    # if not os.path.isdir('train'):
    #     os.mkdir('train')
    #     train_path = os.path.join(out_dir,'train')
    # if not os.path.isdir('val'):
    #     os.mkdir('val')
    #     val_path = os.path.join(out_dir,'val')

    # creating training dataset
    create_dataset(train=True,out_dir=out_dir,text_files=text_files)

    # creating validation dataset
    create_dataset(train=False,out_dir=out_dir,text_files=text_files)


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
