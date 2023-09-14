# 기 학습되어 완성된 yolo 모델 설정 후 진행
# detect 위해서는 yolov5 파일 필요
# pytorch 는 yolov5 패키지 pip로 제공함 : pip install yolov5

import yolov5
import torch
import os
from PIL import Image as I
from django.conf import settings

def y_detect(img, img_name):
    # model = yolov5.load('y5_model/best.pt')  # yolov5 라이브러리 사용방법
    # model.conf = 0.5  # confidence
    # model.iou = 0.45  # IOU Threshold
    # model.multi_label = False
    # model.max_det = 1000  # 객체 최대 도출 개수
    # model = torch.hub.load('ultralytics/yolov5', 'custom', 'y5_model/best.pt')  # 사용자 학습 모델
    img = img
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    results = model(img, size=416)  # 객체 detect
    print(results.pandas().xyxy[0].value_counts('name'))  # 검출된 객체의 이름과 개수 시리즈로 반환
    
    results.render()  # 출력된 결과의 이미지 사용할 수 있게 변환(np.array 형식으로 변환)  
    static_folder = 'media/'
    inferenced_img_dir = os.path.join(
        static_folder, "inferenced_image")  # detect 이미지 저장 경로
    if not os.path.exists(inferenced_img_dir):
        os.makedirs(inferenced_img_dir)  # 없다면 만들어라
    for img in results.ims:  # np.array
            img_base64 = I.fromarray(img)  # 이미지 형식으로 변환
            img_base64.save(
                f"{inferenced_img_dir}/{img_name}")  # 이곳에 저장
    res_url = "inferenced_image"+"/" + img_name  # 객체 검출 결과 이미지 저장 경로
    return res_url

    