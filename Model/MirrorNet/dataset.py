"""
 @Time    : 10/2/19 18:00
 @Author  : TaylorMei
 @Email   : mhy666@mail.dlut.edu.cn
 
 @Project : ICCV2019_MirrorNet
 @File    : dataset.py
 @Function: prepare data for training.
 
"""
import os
import os.path
import torch.utils.data as data
from PIL import Image

def make_dataset(root):
    image_path = os.path.join(root, 'Images') #!
    mask_path = os.path.join(root, 'Seg') #!
    img_list = [os.path.splitext(f)[0] for f in os.listdir(image_path) if f.endswith('.jpg')]
    return [
        (os.path.join(image_path, img_name + '.jpg'), os.path.join(mask_path, img_name + '.png'))
        for img_name in img_list]
#def make_dataset(data_path):
#    img_list = [os.path.splitext(f)[0] for f in os.listdir(os.path.join(data_path, 'image')) if f.endswith('.jpg')]
#    return [
#            (os.path.join(data_path, 'image', img_name + '.jpg'), os.path.join(data_path, 'mask', img_name + '.png'))
#            for img_name in img_list]


class ImageFolder(data.Dataset):
    def __init__(self, root, joint_transform=None, img_transform=None, target_transform=None):
        self.root = root
        self.imgs = make_dataset(root)
        self.joint_transform = joint_transform
        self.img_transform = img_transform
        self.target_transform = target_transform

    def __getitem__(self, index):
        img_path, gt_path = self.imgs[index]
        img = Image.open(img_path).convert('RGB')
        target = Image.open(gt_path).convert('L')
        if self.joint_transform is not None:
            img, target = self.joint_transform(img, target)
        if self.img_transform is not None:
            img = self.img_transform(img)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target

    def __len__(self):
        return len(self.imgs)
