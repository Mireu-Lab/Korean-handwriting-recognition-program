# ---

import os
import shutil
import sqlite3
import numpy as np
from PIL import Image
from tqdm import tqdm


# ---
print("-"*10, end="")
print(" SQL 라벨링 Start ", end="")
print("-"*10, end="\n")

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


print("-"*10, end="")
print(" SQL 라벨링 End ")
print("-"*10, end="\n")


# ---


print("-"*10, end="")
print(" numpy 변환 Start ", end="")
print("-"*10, end="\n")


dirList = os.listdir("../dataset_dir/13.한국어글자체/image") # 이미지 레이어 리스트
dirList = sorted(dirList) # 가나다 순으로 정렬


all_dataset_tensor = np.array([]) # 데이터셋 전체
dir_num = 1


for dir in tqdm(dirList):
    fileList = os.listdir(f"../dataset_dir/13.한국어글자체/image/{dir}/") # 디랙토리 파일 리스트


    # npy 파일 저장 디랙토리 생성
    try:
        os.mkdir(f"../dataset_dir/13.한국어글자체/image_npy/{dir}") # 디렉토리 생성
    except FileExistsError:
        pass


    # 이미지 업스케일링 파일 저장 디랙토리 생성
    try:
        os.mkdir(f"../dataset_dir/13.한국어글자체/new_image/{dir}") # 디렉토리 생성
    except FileExistsError:
        pass

    all_dataset_tensor = np.array([]) # 데이터셋 레이블


    for file in fileList:
        imageData = Image.open(f"""../dataset_dir/13.한국어글자체/image/{dir}/{file}""").convert("L") # 이미지 tensor 데이터 출력
        imageData = imageData.resize((200, 200)) # 이미지 업스케일링

        imageData.save(f"""../dataset_dir/13.한국어글자체/new_image/{dir}/{file}""") # 이미지 업스케일링 이미지 저장

        file_tensor = np.array(imageData) # 이미지 tensor 변환
        file_tensor = file_tensor.reshape(-1) # tensor 1차원 변환

        all_dataset_tensor = np.r_[all_dataset_tensor, file_tensor] # 전체 데이터셋 2차원 row 추가
        dir_dataset_tensor = np.r_[dir_dataset_tensor, file_tensor] # 레이블 데이터셋 2차원 row 추가

        np.save(f"""../dataset_dir/13.한국어글자체/image_npy/{dir}/{file[:-4]}""", file_tensor) # 이미지 데이터셋 파일 .npy 저장
    
    np.save(f"../dataset_dir/13.한국어글자체/label_npy/{dir}/{dir_num}.{dir}", dir_dataset_tensor) # 레이블 데이터셋 파일 .npy 저장
    
    dir_num += 1

np.save(f"../dataset_dir/13.한국어글자체/label_npy/0.한국어_손글씨_데이터", all_dataset_tensor) # 전체 데이터셋 .npy 저장

print("-"*10, end="")
print(" numpy 변환 End ", end="")
print("-"*10, end="\n")