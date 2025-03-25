import os
from dotenv import load_dotenv
from azure.cognitiveservices.vision.face import FaceClient
#from azure.cognitiveservices.vision.face.models import FaceDetectionModel, FaceRecognitionModel
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image, ImageDraw

# 환경변수 로드
load_dotenv()
endpoint = os.getenv("FACE_API_ENDPOINT")
key = os.getenv("FACE_API_KEY")

# FaceClient 인스턴스 생성
face_client = FaceClient(endpoint, CognitiveServicesCredentials(key))

# 이미지 경로
image_path = "test_samples/sample.jpg"

# 얼굴 감지 실행
with open(image_path, "rb") as image_data:
    faces = face_client.face.detect_with_stream(
        image=image_data,
        detection_model="detection_03",
        recognition_model="recognition_04",
        return_face_id=False  # 얼굴 ID 필요 없으면 False
    )

# 얼굴 감지 결과 확인
if not faces:
    print("얼굴을 찾을 수 없습니다.")
else:
    print(f"얼굴 {len(faces)}개 감지됨")

    # 이미지 열기 및 그리기 준비
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for i, face in enumerate(faces, start=1):
        rect = face.face_rectangle
        left = rect.left
        top = rect.top
        right = left + rect.width
        bottom = top + rect.height

        # 사각형 그리기
        draw.rectangle([(left, top), (right, bottom)], outline="red", width=4)
        draw.text((left, top - 10), f"Face {i}", fill="red")

        print(f"- 얼굴 {i}: 위치 (x={left}, y={top}, w={rect.width}, h={rect.height})")

# 바운딩 박스 그리기 끝난 후에:
output_path = "output_face_detected.jpg"

# RGBA 모드이면 RGB로 변환
if image.mode == "RGBA":
    image = image.convert("RGB")

image.save(output_path)
print(f"\n 결과 이미지 저장됨: {output_path}")
