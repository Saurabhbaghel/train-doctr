import numpy as np
import cv2 as cv
import glob
import random
import os

class deform:
  def __init__(self):
      self.fonts = glob.glob('./fonts/*.ttf')
      

  def gaussian_blur(self,image):
    kernel = (1,1)
    return cv.GaussianBlur(image,kernel, 0)

  def median_blur(self,image):
    return cv.medianBlur(image,3)

  def gaussian_noise(self,image):
    mean = 0
    var = 0.1
    sigma = var**0.5
    gauss = np.random.normal(mean,sigma,image.shape)
    gauss.reshape(image.shape)
    return image + gauss

  def salt_pepper_noise(self,image):
    sp = np.copy(image)
    amt = 5e-01
    coords = [np.random.randint(0,i-1,int(amt*image.size)) for i in image.shape]
    sp[coords] = 255
    return sp

  def fonts(self,num_of_fonts):
    """

    :param num_of_fonts: the number of fonts to choose from
    :return: selected choices
    """
    choices = random.choices(self.fonts,5)
    return choices


  def all_fonts(self):
    li = []
    for font in self.fonts:
      li.append(os.path.basename(font))
    return li


  def add_deformity(self,image):
    """

    :param image: raw image
    :return: deformed image
    """
    nums=random.choices(range(4),k=2)
    switch = {
        0:'gaussian_blur',
        1:'median_blur',
        2:'gaussian_noise',
        3:'salt_pepper_noise'
    }
    for n in nums:
      deformity=switch.get(n)
      if deformity == 'gaussian_blur': return self.gaussian_blur(image)
      elif deformity == 'median_blur': return self.median_blur(image)
      elif deformity == 'gaussian_noise': return self.gaussian_noise(image)
      else:
        for i in range(2):
          image = self.salt_pepper_noise(image)
        return image
