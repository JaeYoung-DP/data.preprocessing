# KR-DBNet
Ship string detection

ship_crop (선박 데이터 디버깅 과정) 
 - img_count.py 하위폴더들의 이미지 총 갯수를 카운트 합니다.
 - bbox_ori_img_all.py 를 통해 이미지의 모든 바운딩 박스를 이미지에 표현합니다.
 - find_json_empty.py 이미지와 json의 매칭을 통해 매칭되지 않는 이미지와 json을 찾아냅니다.
 - resize_all.py는 원본 이미지의 크기가 크기 때문에 모델의 입력으로 입력시 소요시간 및 데이터 전처리 과정에서의 문제점이 있습니다. 이러한 문제점을 해결하고자 선박의 영역에 맞는 bbox의 크기만큼 선박을 잘라내는 과정입니다.
 - resize_check.py를 통해 잘라낸 선박의 이미지를 시각화하고 기존의 json에서의 변경된 label을 확인합니다. ( crop하는 과정에서의 label 오류가 발생할 수 있기 때문에 디버깅 과정의 일종입니다. )
 - young_json2txt.py/create_json.py = mmocr / github-DBNet에 맞는 label로 변환하기 위해 json형식의 annotation file을 txt형식으로 변환하고 create_json.py를 통해 mmocr의 annotation형식으로 변환합니다.

 
