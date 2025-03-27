# python=3.11 / 2025년 3월 27일 기준 python 3.13와 OpenCV 호환이 별로 안좋음
import cv2

# 이미지 불러오기
image_path = "./test_samples/sample.jpg"
image = cv2.imread(image_path)

# 이미지가 정상적으로 로드되었는지 확인
if image is None:
    raise FileNotFoundError(f"이미지를 찾을 수 없습니다: {image_path}")

# 얼굴 인식용 Haar Cascade 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
if face_cascade.empty():
    raise IOError("Haar cascade xml 파일을 불러오지 못했습니다.")

# 이미지 그레이스케일로 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 얼굴 감지
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# 감지된 얼굴 영역에 모자이크 처리
for (x, y, w, h) in faces:
    face_roi = image[y:y+h, x:x+w]
    
    # 모자이크: 이미지 축소 후 다시 확대
    mosaic_rate = 0.05  # 0.05 = 5% 크기로 축소
    small = cv2.resize(face_roi, (0, 0), fx=mosaic_rate, fy=mosaic_rate, interpolation=cv2.INTER_LINEAR)
    mosaic_face = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

    # 원본 이미지에 모자이크 덮어쓰기
    image[y:y+h, x:x+w] = mosaic_face

# 결과 이미지 저장 또는 출력
cv2.imwrite("./test_samples/output_mosaic.jpg", image)
cv2.imshow("Mosaic Face", image)
cv2.waitKey(0)
cv2.destroyAllWindows()