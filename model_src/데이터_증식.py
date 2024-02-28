
from tensorflow.keras.preprocessing import image

datagen = image.ImageDataGenerator(
    rotation_range=30,
    # 지정된 각도 범위 내에서 임의로 원본이미지를 회전
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,  # 지정된 이동범위 내(%비율)에서 원본이미지를 확대/축소
    vertical_flip=True,
    horizontal_flip=True,
    # 상하 좌우 반전 ( 이미지 증식시 다른 비슷한 이미지가 아닌 다른 이미지로 간주)
    fill_mode="wrap",  # 이미지를 변형시키면 틀었을때 빈공간을 주변 pixel로 채운다
)


def fileProliferation(dir, file):
    # 이미지를 가져온다
    img = image.load_img(
        f"../dataset_dir/new_image/{dir}/{file}",
        target_size=(50, 50),
    )

    # 이미지를 array로 변형
    img_arr = image.img_to_array(img)
    img_arr = img_arr.reshape((1,) + img_arr.shape)

    # 도화지 그리기
    idx = 0
    for batch in datagen.flow(img_arr, batch_size=32):
        img2 = image.array_to_img(batch[0])
        img2.save(f"../dataset_dir/new_image/{dir}/{file[:-4]}_{idx}.png", "png")
        
        if idx == 100:
            break
        
        idx += 1


import os
from tqdm import tqdm

dirList = ["가", "나", "다", "라", "마", "바", "아", "자", "차", "카", "타", "파", "하"]

for dir in tqdm(dirList):
    fileList = os.listdir(f"../dataset_dir/new_image/{dir}/") # 디랙토리 파일 리스트
    
    for file in fileList:
        fileProliferation(dir, file)
