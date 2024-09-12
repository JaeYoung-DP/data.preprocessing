import os
from PIL import Image, ImageFile
import json

ImageFile.LOAD_TRUNCATED_IMAGES = True

# 'cropped_images' 폴더 생성
cropped_images_base_dir = './sibar'
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

def process_image_and_annotation(img_path, ann_path):
    global img_count, subfolder_index, current_subfolder_path
    
    try:
        # 어노테이션 파일에서 JSON 데이터 읽기
        with open(ann_path, 'r') as f:
            json_data = json.load(f)
        
        # JSON에서 'regions'를 순회하며 "문자" 태그가 아닌 영역의 좌표 데이터 추출
        for region in json_data['regions']:
            if region['tags'][0] != "문자" or (len(region['tags']) > 1 and region['tags'][1] != "문자"):
                points = region['points']

                x1, y1 = points[0]['x'], points[0]['y']
                x2, y2 = points[1]['x'], points[1]['y']
                x3, y3 = points[2]['x'], points[2]['y']
                x4, y4 = points[3]['x'], points[3]['y']

                # 좌표 확인
                print(f"Original coordinates: ({x1}, {y1}), ({x2}, {y2}), ({x3}, {y3}), ({x4}, {y4})")

                with Image.open(img_path) as img:
                    # 이미지 크기 확인
                    print(f"Image size: {img.size}")

                    # 잘라낼 영역 지정
                    cropped_img = img.crop((x1, y1, x3, y3))

                    # 잘라낸 이미지 크기 확인
                    print(f"Cropped image size: {cropped_img.size}")
                    print(f"{x3-x1},{y3-y1}")

                    # 파일명 생성
                    basename = os.path.basename(img_path)
                    cropped_filename = basename.replace('.jpg', '_cropped.jpg')
                    # 잘라낸 이미지 저장 경로
                    cropped_img_path = os.path.join(current_subfolder_path, cropped_filename)
                    # 잘라낸 이미지 저장
                    cropped_img.save(cropped_img_path)

                    # 이미지 카운트 증가 및 필요시 새 서브 폴더 생성
                    img_count += 1
                    if img_count % 5000 == 0:
                        subfolder_index += 1
                        current_subfolder_path = get_subfolder_path(cropped_images_base_dir, subfolder_index)
                        if not os.path.exists(current_subfolder_path):
                            os.makedirs(current_subfolder_path)
    except ValueError as e:
        print(f"오류: {e}, 파일: {img_path}")

# 예시 이미지 및 어노테이션 파일 경로
img_path = '/home/workspace/202309071528_┤δ├╡╟╫_└║╝║╚ú_31704558_0000001216.jpg'
ann_path = '/home/workspace/202309071528_┤δ├╡╟╫_└║╝║╚ú_31704558_0000001216.json'

# 이미지와 어노테이션 파일 처리
process_image_and_annotation(img_path, ann_path)
