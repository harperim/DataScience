from django.shortcuts import render
import os 
from django.core.files.storage import FileSystemStorage
from uuid import uuid4   # 고유번호 생성 라이브러리
from . import yolov5_detect

# Create your views here.
def index(request):
    return render(request, 'detect/img_up_res.html')  # html 파일 연결

# 이미지 및 파일 저장
def rename_imgfile_to_uuid(filename) :  # 고유번호 이용해서 이미지 파일명 변경하는 함수
    ext = filename.split('.')[-1]  # 확장자 분리
    uuid = uuid4().hex
    filename = '{}.{}'.format(uuid, ext)
    return filename


def detect(request):  # 전달된 이미지를 받아서 yolo 모델에 주입 후 검출된 결과 이미지를 클라이언트에게 전송
    img = request.FILES.get('images')  # 사용자가 전송한 이미지 파일 갖고 오기
    fs = FileSystemStorage()  # 파일 저장소 접근 객체
    # 전송된 파일명 변경해서 저장 (서버에서 사용할 유일한 파일명 생성)ㅋㅋ
    file_name = rename_imgfile_to_uuid(img.name)
    img_up_url = fs.save(file_name, img)  # media 디렉터리에 저장
    print(img_up_url)
    img = 'media/' + img_up_url
    
    # 이미지 객체 검출 함수 호출 
    res_url = yolov5_detect.y_detect(img, img_up_url)
    print(res_url)
    return render(request, 'detect/result.html', {'image' : res_url})
