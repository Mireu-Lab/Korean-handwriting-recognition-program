import os
import numpy as np
from PIL import Image
from tqdm import tqdm

dirList = os.listdir("../dataset_dir/image") # 이미지 레이어 리스트
dirList = sorted(dirList) # 가나다 순으로 정렬


for dir in tqdm(dirList):
    fileList = os.listdir(f"../dataset_dir/image/{dir}/") # 디랙토리 파일 리스트

    # 이미지 업스케일링 파일 저장 디랙토리 생성
    try:
        os.mkdir(f"../dataset_dir/new_image/{dir}") # 디렉토리 생성
    except FileExistsError:
        pass

    for file in fileList:
        imageData = Image.open(f"""../dataset_dir/image/{dir}/{file}""").convert("L") # 이미지 tensor 데이터 출력
        imageData = imageData.resize((50, 50)) # 이미지 업스케일링

        imageData.save(f"""../dataset_dir/new_image/{dir}/{file}""") # 이미지 업스케일링 이미지 저장

