import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures

# 환경변수 로드
load_dotenv()

endpoint = os.getenv('COMPUTER_VISION_ENDPOINT')
key = os.getenv('COMPUTER_VISION_KEY')

# 클라이언트 생성
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# 이미지 파일 열기
with open("./test_samples/sample.jpg", "rb") as f:
    image_data = f.read()

# 이미지 분석 요청
result = client.analyze(
    image_data=image_data,
    visual_features=[VisualFeatures.CAPTION,
                     VisualFeatures.TAGS,
                     VisualFeatures.OBJECTS]
)

# 결과 출력
if result.caption is not None:
    print(f"Caption: {result.caption.text} (Confidence: {result.caption.confidence:.2f})")
else:
    print("No caption was generated.")

if result.tags and "values" in result.tags:
    print("Tags:")
    for tag in result.tags["values"]:
        name = tag.get("name", "Unknown")
        confidence = tag.get("confidence", 0.0)
        print(f"- {name} (Confidence: {confidence:.2f})")
else:
    print("No tags were found.")

if result.objects and "values" in result.objects:
    print("Detected Objects:")
    for idx, obj in enumerate(result.objects["values"], start=1):
        print(f"\nObject {idx}:")
        
        # 태그가 여러 개일 수 있으므로 가장 신뢰도 높은 것으로 표시
        best_tag = max(obj["tags"], key=lambda t: t.get("confidence", 0)) if obj.get("tags") else {}
        tag_name = best_tag.get("name", "Unknown")
        tag_conf = best_tag.get("confidence", 0.0)
        print(f"- Label: {tag_name} (Confidence: {tag_conf:.2f})")
        
        # 바운딩 박스 출력
        bbox = obj.get("boundingBox", {})
        x, y = bbox.get("x", 0), bbox.get("y", 0)
        w, h = bbox.get("w", 0), bbox.get("h", 0)
        print(f"- Bounding Box: (x: {x}, y: {y}, width: {w}, height: {h})")
else:
    print("No objects were detected.")
