import os
import shutil
import sqlite3
from tqdm import tqdm

db = sqlite3.connect("../dataset.sqlite")
sql = db.cursor()


lists = os.listdir("../dataset_dir/original/")
lists = sorted(lists, key=lambda boxes: boxes[:-4])


imageText = None


for imageInfo in tqdm(lists):
    try:
        # SQL 구문 검색
        sql.execute(f"""SELECT text FROM `handwriting_dataset` WHERE `image_id` = '{imageInfo[:-4]}'""")
        imageText = sql.fetchone()
    

        # 레이블 디렉토리 생성
        try:
            os.mkdir(f"../dataset_dir/image/{imageText[0]}") # 디렉토리 생성
        except FileExistsError:
            pass


        # 파일 복사
        src = f"../dataset_dir/original/"
        dir = f"../dataset_dir/image/{imageText[0]}/"
        shutil.copyfile(src + imageInfo, dir + imageInfo) # 파일 복사

    except TypeError:
        print(imageInfo, imageText)
