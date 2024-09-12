import io
import os
from PIL import Image, ImageFile
import json
import natsort
from tqdm import tqdm
import time

ImageFile.LOAD_TRUNCATED_IMAGES = True

# 'cropped_images' 폴더 생성
cropped_images_base_dir = './stella2_resize_all'
if not os.path.exists(cropped_images_base_dir):
    os.makedirs(cropped_images_base_dir)

# 이미지 카운트 및 서브 폴더 인덱스 초기화
img_count = 0
subfolder_index = 1

def get_subfolder_path(base_dir, index):
    # 새로운 서브 폴더 경로 생성
    return os.path.join(base_dir, str(index))

# 현재 서브 폴더 생성
current_subfolder_path = get_subfolder_path(cropped_images_base_dir, subfolder_index)
if not os.path.exists(current_subfolder_path):
    os.makedirs(current_subfolder_path)

folder_path_list_1 = []
folder_path_list_2 = []
filename_list = []
annotation_list = []

i = 0
j = 0

for folder_path_1 in natsort.natsorted(os.listdir('./stella_data2')):
    folder_path_list_1.append(folder_path_1)
    for folder_path_2 in natsort.natsorted(os.listdir('./stella_data2/{}'.format(folder_path_list_1[i]))):
        folder_path_list_2.append(folder_path_2)
        filename = './stella_data2/{}/{}/Images'.format(folder_path_list_1[i], folder_path_list_2[j])
        annotation = './stella_data2/{}/{}/Annotations'.format(folder_path_list_1[i], folder_path_list_2[j])
        filename_list.append(filename)
        annotation_list.append(annotation)
        j = j + 1
    i = i + 1

img_path_list = []
ann_path_list = []

k = 0

while k < len(filename_list):
    img_files = natsort.natsorted(os.listdir(filename_list[k]))
    ann_files = natsort.natsorted(os.listdir(annotation_list[k]))
    if len(img_files) != len(ann_files):
        print(f"Warning: Mismatch in number of image and annotation files in {filename_list[k]}")
    
    img_path_list.extend([os.path.join(filename_list[k], img_file) for img_file in img_files])
    ann_path_list.extend([os.path.join(annotation_list[k], ann_file) for ann_file in ann_files])

    k = k + 1

log_file_path = './plz.txt'
with open(log_file_path, 'w') as log_file:
    for img_path, ann_path in zip(img_path_list, ann_path_list):
        try:
            with open(ann_path, 'r') as f:
                json_data = json.load(f)

            for region in json_data['regions']:
                if region['tags'][0] != "문자" or (len(region['tags']) > 1 and region['tags'][1] != "문자"):
                    bounding_box = region.get('boundingBox', None)
                    if bounding_box:
                        left = bounding_box['left']
                        top = bounding_box['top']
                        right = left + bounding_box['width']
                        bottom = top + bounding_box['height']
                    else:
                        points = region['points']
                        x_coords = sorted([points[0]['x'], points[1]['x'], points[2]['x'], points[3]['x']])
                        y_coords = sorted([points[0]['y'], points[1]['y'], points[2]['y'], points[3]['y']])
                        left, top, right, bottom = x_coords[0], y_coords[0], x_coords[2], y_coords[2]

                    log_file.write(f"Cropping area: ({left}, {top}), ({right}, {bottom})\n")

                    with Image.open(img_path) as img:
                        #log_file.write(f"Image size: {img.size}\n")

                        cropped_img = img.crop((left, top, right, bottom))

                        #log_file.write(f"Cropped image size: {cropped_img.size}\n")

                        basename = os.path.basename(img_path)
                        cropped_filename = basename.replace('.jpg', '.jpg')
                        cropped_img_path = os.path.join(current_subfolder_path, cropped_filename)
                        cropped_img.save(cropped_img_path)

                        img_count += 1
                        if img_count % 5000 == 0:
                            subfolder_index += 1
                            current_subfolder_path = get_subfolder_path(cropped_images_base_dir, subfolder_index)
                            if not os.path.exists(current_subfolder_path):
                                os.makedirs(current_subfolder_path)
        except ValueError as e:
            log_file.write(f"오류: {e}, 파일: {img_path}\n")
            continue

#print(f"Cropping area: ({left}, {top}), ({right}, {bottom})")
#print(f"Image size: {img.size}")
#print(f"Cropped image size: {cropped_img.size}")
