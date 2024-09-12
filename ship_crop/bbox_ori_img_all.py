import os
import shutil
import json
from PIL import Image, ImageDraw
import natsort

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

k = 0
img_counter = 0
folder_counter = 1

# 첫 번째 폴더 생성
current_folder = './stella2_bbox/{}'.format(folder_counter)
os.makedirs(current_folder, exist_ok=True)

while k < len(filename_list):
    for img_path, ann_path in zip(natsort.natsorted(os.listdir(filename_list[k])), natsort.natsorted(os.listdir(annotation_list[k]))):
        # 이미지 경로와 주석 경로를 가져옴
        original_img_path = os.path.join(filename_list[k], img_path)
        annotation_path = os.path.join(annotation_list[k], ann_path)

        try:
            with open(annotation_path, "r") as file:
                data = json.load(file)

                for region in data.get('regions', []):
                    points = region.get('points', [])
                    tag = region.get('tags', [])
                    attributes = region.get("attributes", {})
                    character = attributes.get("Character", None)

                    if len(points) < 4 or not character:
                        # 조건에 맞지 않는 경우에만 처리
                        # 또는 '문자' 태그가 없는 경우
                        # 바운딩 박스 그리기
                        img = Image.open(original_img_path)
                        draw = ImageDraw.Draw(img)

                        x_values = [point['x'] for point in points]
                        y_values = [point['y'] for point in points]

                        x_min = min(x_values)
                        x_max = max(x_values)
                        y_min = min(y_values)
                        y_max = max(y_values)

                        # 바운딩 박스 그리기
                        draw.rectangle((x_min, y_min, x_max, y_max), outline=(0, 255, 0), width=3)
                        
                        # 이미지 저장 경로 설정
                        save_path = os.path.join(current_folder, os.path.basename(original_img_path))
                        img.save(save_path)

                        img_counter += 1

                        # 이미지 카운터가 10,000에 도달하면 새로운 폴더 생성
                        if img_counter == 10000:
                            folder_counter += 1
                            current_folder = './stella2_bbox/{}'.format(folder_counter)
                            os.makedirs(current_folder, exist_ok=True)
                            img_counter = 0  # 이미지 카운터 초기화

                    # 한 이미지에 대한 처리가 끝나면 루프를 빠져나옴
                    break
        except Exception as e:
            print(f"Error processing image: {original_img_path}")
            print(f"Annotation file: {annotation_path}")
            print(f"Error: {e}")
            # 추가로 필요한 정보가 있다면 여기에 추가할 수 있습니다.
            continue
    k = k + 1
