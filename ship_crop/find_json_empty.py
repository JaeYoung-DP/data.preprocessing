import os

def find_non_json_files_in_annotations_folder(root_folder):
    non_json_files = []

    for root, dirs, files in os.walk(root_folder):
        if 'Annotations' in dirs:
            annotation_folder = os.path.join(root, 'Annotations')
            for sub_root, sub_dirs, sub_files in os.walk(annotation_folder):
                for file in sub_files:
                    if not file.endswith('.json'):
                        file_path = os.path.join(sub_root, file)
                        non_json_files.append(file_path)

    return non_json_files

root_folder = './stella_data2'
non_json_files = find_non_json_files_in_annotations_folder(root_folder)

if non_json_files:
    print("JSON이 아닌 파일을 찾았습니다:")
    for file in non_json_files:
        print(file)
else:
    print("JSON이 아닌 파일을 찾지 못했습니다.")
