import os
import shutil
import sqlite3

db = sqlite3.connect("../dataset.sqlite")
sql = db.cursor()


lists = os.listdir("../dataset_dir/13.한국어글자체/original/")
lists = sorted(lists, key=lambda boxes: boxes[:-4])


imageText = None


for imageInfo in tqdm(lists):
    try:
        # SQL 구문 검색
        sql.execute(f"""SELECT text FROM `handwriting_dataset` WHERE `image_id` = '{imageInfo[:-4]}'""")
        imageText = sql.fetchone()
    

        # 레이블 디렉토리 생성
        try:
            os.mkdir(f"../dataset_dir/13.한국어글자체/image/{imageText[0]}") # 디렉토리 생성
        except FileExistsError:
            pass


        # 파일 복사
        src = f"../dataset_dir/13.한국어글자체/original/"
        dir = f"../dataset_dir/13.한국어글자체/image/{imageText[0]}/"
        shutil.copyfile(src + imageInfo, dir + imageInfo) # 파일 복사

    except TypeError:
        print(imageInfo, imageText)


print("="*20)
"""
이미지 업스케일링
"""

import os
import numpy as np
from PIL import Image
from tqdm import tqdm

dirList = os.listdir("../dataset_dir/13.한국어글자체/image") # 이미지 레이어 리스트
dirList = sorted(dirList) # 가나다 순으로 정렬


for dir in tqdm(dirList):
    fileList = os.listdir(f"../dataset_dir/13.한국어글자체/image/{dir}/") # 디랙토리 파일 리스트

    # 이미지 업스케일링 파일 저장 디랙토리 생성
    try:
        os.mkdir(f"../dataset_dir/13.한국어글자체/new_image/{dir}") # 디렉토리 생성
    except FileExistsError:
        pass

    for file in fileList:
        imageData = Image.open(f"""../dataset_dir/13.한국어글자체/image/{dir}/{file}""").convert("L") # 이미지 tensor 데이터 출력
        imageData = imageData.resize((200, 200)) # 이미지 업스케일링

        imageData.save(f"""../dataset_dir/13.한국어글자체/new_image/{dir}/{file}""") # 이미지 업스케일링 이미지 저장


print("="*20)
"""
이미지 numpy화
"""

import os
import numpy as np
from PIL import Image
from tqdm import tqdm

dirList = os.listdir("../dataset_dir/13.한국어글자체/image") # 이미지 레이어 리스트
dirList = sorted(dirList) # 가나다 순으로 정렬

for dir in tqdm(dirList):
    fileList = os.listdir(f"../dataset_dir/13.한국어글자체/image/{dir}/") # 디랙토리 파일 리스트

    # npy 파일 저장 디랙토리 생성
    try:
        os.mkdir(f"../dataset_dir/13.한국어글자체/image_npy/{dir}") # 디렉토리 생성
    except FileExistsError:
        pass

    dir_dataset_tensor = [] # 데이터셋 레이블
    dir_label_tensor = [] # 데이터셋 레이블

    for file in fileList:
        tensor_label = dict.fromkeys(dirList, 0) # 12000개의 str 값을 0으로 초기화하는 dict 생성
        tensor_label[dir[:-4]] = 1 # 사용자가 지정한 str 값을 1로 변경
        tensor_label = list(tensor_label.values())

        dir_label_tensor.append([tensor_label]) # 레이블 2차원 row 추가

        imageData = Image.open(f"""../dataset_dir/13.한국어글자체/image/{dir}/{file}""").convert("L") # 이미지 tensor 데이터 출력
        imageData = imageData.resize((200, 200)) # 이미지 업스케일링

        file_tensor = np.array(imageData) # 이미지 tensor 변환
        file_tensor = file_tensor.reshape(-1) # tensor 1차원 변환

        dir_dataset_tensor.append(file_tensor.tolist()) # 레이블 데이터셋 2차원 row 추가

        np.save(f"""../dataset_dir/13.한국어글자체/image_npy/{dir}/{file[:-4]}_data""", file_tensor) # 이미지 데이터셋 파일 .npy 저장
    np.save(f"""../dataset_dir/13.한국어글자체/image_npy/{dir}/{file[:-4]}_label""", dir_label_tensor) # 이미지 레이블 파일 .npy 저장