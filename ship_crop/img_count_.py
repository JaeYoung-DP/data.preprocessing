import os
import natsort
import shutil

folder_path_list_1 = []
folder_path_list_2 = []
filename_list = []
annotation_list = []

i = 0
j = 0

# 원본 이미지 경로를 저장할 리스트
original_img_path_list = []

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
current_folder = './stella2_count/{}'.format(folder_counter)
os.makedirs(current_folder, exist_ok=True)

while k < len(filename_list):
    for img_path in natsort.natsorted(os.listdir(filename_list[k])):
        # 이미지 경로를 리스트에 추가
        original_img_path = os.path.join(filename_list[k], img_path)
        original_img_path_list.append(original_img_path)
        
        # 이미지를 현재 폴더로 복사
        shutil.copy(original_img_path, current_folder)
        
        img_counter += 1
        
        # 이미지 카운터가 10,000에 도달하면 새로운 폴더 생성
        if img_counter == 10000:
            folder_counter += 1
            current_folder = './stella2_count/{}'.format(folder_counter)
            os.makedirs(current_folder, exist_ok=True)
            img_counter = 0  # 이미지 카운터 초기화
    k = k + 1

