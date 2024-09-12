import io
import os
from PIL import Image, ImageFile, ImageDraw
import json
import natsort
from glob import glob
from tqdm import tqdm
import time
ImageFile.LOAD_TRUNCATED_IMAGES = True

folder_path_list_1 = []
folder_path_list_2 = []
filename_list = []
annotation_list = []

i = 0
j = 0

for folder_path_1 in natsort.natsorted(os.listdir('./stella_data')):
    folder_path_list_1.append(folder_path_1)
    for folder_path_2 in natsort.natsorted(os.listdir('./stella_data/{}'.format(folder_path_list_1[i]))):
        folder_path_list_2.append(folder_path_2)
        filename = './stella_data/{}/{}/Images'.format(folder_path_list_1[i], folder_path_list_2[j])
        annotation = './stella_data/{}/{}/Annotations'.format(folder_path_list_1[i], folder_path_list_2[j])
        filename_list.append(filename)
        annotation_list.append(annotation)
        j = j + 1
    i = i + 1

img_path_list = []
ann_path_list = []

k = 0
l = 0

while k < len(filename_list):
    for img_path in natsort.natsorted(os.listdir(filename_list[k])):
        img_path_list.append(os.path.join(filename_list[k], img_path))
    for ann_path in natsort.natsorted(os.listdir(annotation_list[k])):
        ann_path_list.append(os.path.join(annotation_list[k], ann_path))
    k = k + 1

for Ann_path_list in ann_path_list:
    ori_img_name = os.path.basename(Ann_path_list).split('.')
    with open(Ann_path_list, "r") as file:
        data = json.load(file)
        ship_point_list = []

        if not data['regions'] or len(data['regions']) < 2:
            continue
        else :
            for p, q in enumerate(data['regions']):
                point_list = []
                point = q['points']
                tags = q['tags'] # 여기서 'tags'로 변경
                attributes = q["attributes"]

                for tag in tags:# 여기서 for문 추가
                    try: 
                        if tag != '문자':
                            x1, y1 = point[0].values()
                            x2, y2 = point[1].values()
                            x3, y3 = point[2].values()
                            x4, y4 = point[3].values()
                            spl = [x1, y1, x2, y2, x3, y3, x4, y4]
                            ship_point_list.extend(spl)
                            continue
                        else:
                            x1, y1 = point[0].values()
                            x2, y2 = point[1].values()
                            x3, y3 = point[2].values()
                            x4, y4 = point[3].values()
                            character = attributes["Character"]
                            if character == "":
                                character = "###"

                            pl = [x1, y1, x2, y2, x3, y3, x4, y4]
                            point_list.extend(pl)
                            
                        if point_list and ship_point_list:
                            X1 = int(point_list[0] - ship_point_list[0])
                            Y1 = int(point_list[1] - ship_point_list[1])

                            X2 = int(point_list[2] - ship_point_list[0])
                            Y2 = int(point_list[3] - ship_point_list[1])

                            X3 = int(point_list[4] - ship_point_list[0])
                            Y3 = int(point_list[5] - ship_point_list[1])

                            X4 = int(point_list[6] - ship_point_list[0])
                            Y4 = int(point_list[7] - ship_point_list[1])

                            path = '/home/workspace/tag_resize_images/1/{}.jpg'.format(ori_img_name[0])

                            if os.path.exists(path):
                                img = Image.open('/home/workspace/tag_resize_images/1/{}.jpg'.format(ori_img_name[0]))
                                draw = ImageDraw.Draw(img)
                                draw.rectangle((X1, Y1, X3, Y3), outline=(0,255,0), width = 3)
                                img.save('/home/workspace/t_i/{}.jpg'.format(ori_img_name[0]))

                                with open('/home/workspace/t_g/{}.txt'.format(ori_img_name[0]), 'a') as t:
                                    t.write('{},{},{},{},{},{},{},{},{}\n'.format(X1, Y1, X2, Y2, X3, Y3, X4, Y4, character))
                    except ValueError as e:
                        print(f"오류 발생: {e}. 해당 그림은 건너뜁니다.")
