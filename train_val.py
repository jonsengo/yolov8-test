# -*- coding: gbk -*-
#用于将图片和标注文件 随机分配到 训练集 

import os
import random
import shutil

def split_images(images_input_folder,labels_input_folder, output_images_train_folder, output_images_val_folder,output_labels_train_folder,output_labels_val_folder, split_ratio):
    if not os.path.exists(output_images_train_folder):
        os.makedirs(output_images_train_folder)
    if not os.path.exists(output_images_val_folder):
        os.makedirs(output_images_val_folder)
        
    if not os.path.exists(output_labels_train_folder):
        os.makedirs(output_labels_train_folder)
    if not os.path.exists(output_labels_val_folder):
        os.makedirs(output_labels_val_folder)        
        

    image_files = [f for f in os.listdir(images_input_folder) if f.lower().endswith('.jpg')]
    random.shuffle(image_files)

    train_count = int(len(image_files) * split_ratio)
    train_files = image_files[:train_count]
    val_files = image_files[train_count:]
    #处理 图片 images 文件夹
    for train_file in train_files:
        input_path = os.path.join(images_input_folder, train_file)
        output_path = os.path.join(output_images_train_folder, train_file)
        shutil.move(input_path, output_path)
        print(f"Moved {train_file} to {output_images_train_folder}")

    for val_file in val_files:
        input_path = os.path.join(images_input_folder, val_file)
        output_path = os.path.join(output_images_val_folder, val_file)
        shutil.move(input_path, output_path)
        print(f"Moved {val_file} to {output_images_val_folder}")

    #处理 labels 文件夹
    train_labels_txt = [filename.replace(".jpg", ".txt") for filename in train_files]
    val_labels_txt = [filename.replace(".jpg", ".txt") for filename in val_files]
    
    for train_label in train_labels_txt:
        input_path = os.path.join(labels_input_folder, train_label)
        output_path = os.path.join(output_labels_train_folder, train_label)
        shutil.move(input_path, output_path)
        print(f"Moved {train_label} to {output_labels_train_folder}")    
    
    for val_label in val_labels_txt:
        input_path = os.path.join(labels_input_folder, val_label)
        output_path = os.path.join(output_labels_val_folder, val_label)
        shutil.move(input_path, output_path)
        print(f"Moved {val_label} to {output_labels_val_folder}")    
    
if __name__ == "__main__":
    images_input_folder = "images"
    labels_input_folder = "labels"
    output_images_train_folder = "images/train"
    output_images_val_folder = "images/val"
    output_labels_train_folder = "labels/train"
    output_labels_val_folder = "labels/val"    
    split_ratio = 0.8  # 按照 80% 训练集，20% 验证集的比例划分

    split_images(images_input_folder,labels_input_folder, output_images_train_folder, output_images_val_folder,output_labels_train_folder,output_labels_val_folder, split_ratio)
