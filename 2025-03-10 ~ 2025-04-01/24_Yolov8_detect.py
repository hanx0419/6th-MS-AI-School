# pip install ultralytics

from ultralytics import YOLO

# YOLO 모델 불러오기 (모델 종류: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x 크기에 따른 모델 선택)
model = YOLO("yolov8n.pt")

# 이미지 추론
results = model("./test_samples/sample.jpg", conf=0.5, project="image", save=True)
# 결과 자동 저장 (./image/predict 디렉토리에 이미지 파일 생성)