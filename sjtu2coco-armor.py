"""
YOLO 格式的数据集转化为 COCO 格式的数据集
--root_dir 输入根路径
--save_path 保存文件的名字(没有random_split时使用)
--random_split 有则会随机划分数据集，然后再分别保存为3个文件。
"""

import os
import cv2
import numpy as np
import json
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--root_dir', default='./data',type=str, help="root path of images and labels, include ./images and ./labels and classes.txt")
parser.add_argument('--save_path', type=str,default='./train.json', help="if not split the dataset, give a path to a json file")
parser.add_argument('--random_split', action='store_true', help="random split the dataset, default ratio is 8:1:1")
arg = parser.parse_args()

def train_test_val_split(img_paths,ratio_train=0.1,ratio_test=0,ratio_val=0.2):
    # 这里可以修改数据集划分的比例。
    assert int(ratio_train+ratio_test+ratio_val) == 1
    train_img, middle_img = train_test_split(img_paths,test_size=1-ratio_train, random_state=233)
    ratio=ratio_val/(1-ratio_train)
    val_img, test_img  =train_test_split(middle_img,test_size=ratio, random_state=233)
    print("NUMS of train:val:test = {}:{}:{}".format(len(train_img), len(val_img), len(test_img)))
    return train_img, val_img, test_img
    
def train_val_split(img_paths,ratio_train=0.1,ratio_val=0.2):
    # 这里可以修改数据集划分的比例。
    train_img, val_img = train_test_split(img_paths,test_size=1-ratio_train, random_state=233)
    print("NUMS of train:val = {}:{}".format(len(train_img), len(val_img)))
    return train_img, val_img


def yolo2coco(root_path, random_split):
    originLabelsDir = os.path.join(root_path, 'labels')                                        
    originImagesDir = os.path.join(root_path, 'images')
    with open(os.path.join(root_path, 'classes.txt')) as f:
        classes = f.read().strip().split()
    # images dir name
    indexes = os.listdir(originImagesDir)

    if random_split:
        # 用于保存所有数据的图片信息和标注信息
        train_dataset = {'categories': [], 'annotations': [], 'images': []}
        val_dataset = {'categories': [], 'annotations': [], 'images': []}
        test_dataset = {'categories': [], 'annotations': [], 'images': []}

        # 建立类别标签和数字id的对应关系, 类别id从0开始。
        for i, cls in enumerate(classes, 0):
            train_dataset['categories'].append({'id': i, 'name': cls, 'supercategory': 'mark'})
            val_dataset['categories'].append({'id': i, 'name': cls, 'supercategory': 'mark'})
            test_dataset['categories'].append({'id': i, 'name': cls, 'supercategory': 'mark'})
        train_img, val_img = train_val_split(indexes,0.76,0.24)
    else:
        dataset = {'categories': [], 'annotations': [], 'images': []}
        for i, cls in enumerate(classes, 0):
            dataset['categories'].append({'id': i, 'name': cls, 'supercategory': 'mark'})
    
    # 标注的id
    ann_id_cnt = 0
    for k, index in enumerate(tqdm(indexes)):
        # 支持 png jpg 格式的图片。
        txtFile = index.replace('images','txt').replace('.jpg','.txt').replace('.png','.txt')
        # 读取图像的宽和高
        im = cv2.imread(os.path.join(root_path, 'images/') + index)
        height, width, _ = im.shape
        if random_split:
            # 切换dataset的引用对象，从而划分数据集
                if index in train_img:
                    dataset = train_dataset
                elif index in val_img:
                    dataset = val_dataset
        # 添加图像的信息
        dataset['images'].append({'file_name': index,
                                    'id': k,
                                    'width': width,
                                    'height': height})
        if not os.path.exists(os.path.join(originLabelsDir, txtFile)):
            # 如没标签，跳过，只保留图片信息。
            continue
        # print(txtFile)
        with open(os.path.join(originLabelsDir, txtFile), 'r') as fr:
            labelList = fr.readlines()
            for label in labelList:
                label = label.split(" ")
                H, W, _ = im.shape
                x1 = float(label[1]) * W
                y1 = float(label[2]) * H
                x2 = float(label[3]) * W
                y2 = float(label[4]) * H
                x3 = float(label[5]) * W
                y3 = float(label[6]) * H
                x4 = float(label[7]) * W
                y4 = float(label[8]) * H


                keypoints = np.array([x1, y1, x2, y2, x3, y3, x4, y4])
                num_keypoints = int(len(keypoints) / 2)

                keypoints = keypoints.reshape(-1,2)
                keypoints_type = 2 * np.ones((num_keypoints, 1))
                keypoints = np.concatenate((keypoints,keypoints_type),axis=1)
                keypoints = keypoints.reshape(-1).tolist()

                # 标签序号从0开始计算, coco2017数据集标号混乱，不管它了。
                cls_id = int(label[0])   
                width = max(x1, x2, x3, x4) - min(x1, x2, x3, x4)
                height = max(y1, y2, y3, y4) - min(y1, y2, y3, y4)
                dataset['annotations'].append({
                    'area': width * height,
                    'bbox': [min(x1, x2, x3, x4), min(y1, y2, y3, y4) , width, height],
                    'category_id': cls_id,
                    'id': ann_id_cnt,
                    'image_id': k,
                    'iscrowd': 0,
                    # mask, 矩形是从左上角点按顺时针的四个顶点
                    'segmentation': [[x1, y1, x2, y2, x3, y3, x4, y4]],
                    'num_keypoints': num_keypoints,
                    'keypoints': keypoints
                })
                ann_id_cnt += 1

    # 保存结果
    folder = os.path.join(root_path, 'annotations')
    if not os.path.exists(folder):
        os.makedirs(folder)
    if random_split:
        for phase in ['instances_train2017','instances_val2017','test']:
            json_name = os.path.join(root_path, 'annotations/{}.json'.format(phase))
            with open(json_name, 'w') as f:
                if phase == 'instances_train2017':
                    json.dump(train_dataset, f)
                elif phase == 'instances_val2017':
                    json.dump(val_dataset, f)
                elif phase == 'test':
                    json.dump(test_dataset, f)
            print('Save annotation to {}'.format(json_name))
    else:
        json_name = os.path.join(root_path, 'annotations/{}'.format(arg.save_path))
        with open(json_name, 'w') as f:
            json.dump(dataset, f)
            print('Save annotation to {}'.format(json_name))

if __name__ == "__main__":
    root_path = arg.root_dir
    assert os.path.exists(root_path)
    random_split = arg.random_split
    print("Loading data from ",root_path,"\nWhether to split the data:",random_split)
    yolo2coco(root_path,random_split)
