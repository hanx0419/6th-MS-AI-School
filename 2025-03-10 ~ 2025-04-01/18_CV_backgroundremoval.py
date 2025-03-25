# 2025년 3월 31일 이후로 Azure AI Image Analysis 4.0 Segment API와 배경 제거 서비스가 중단될 예정

import os
import requests
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("COMPUTER_VISION_ENDPOINT")
key = os.getenv("COMPUTER_VISION_KEY")

image_path = "./test_samples/sample.jpg"

url = f"{endpoint}computervision/imageanalysis:segment?api-version=2023-02-01-preview"

param ={"mode" : "backgroundRemoval"}
# backgroundRemoval : 감지된 전경 객체의 이미지를 투명한 배경으로 출력합니다.
# foregroundMatting : 감지된 전경 객체의 불투명도를 나타내는 회색조 알파 매트 이미지를 출력합니다.

query_string = "&".join([f"{k}={v}" for k, v in param.items()])

url_final = url + "&" + query_string

headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Content-Type": "application/octet-stream"
}

with open(image_path, "rb") as f:
    image_data = f.read()

response = requests.post(url_final, headers=headers, data=image_data)

if response.status_code == 200:
    with open("output_no_bg.png", "wb") as out_file:
        out_file.write(response.content)
    print("배경 제거 이미지 저장 완료: output_no_bg.png")
else:
    print(f"요청 실패: {response.status_code}")
    print(response.text)