import cv2
import numpy as np

# 경로 설정
weights_path = './data/yolo3/yolov3.weights'
config_path  = './data/yolo3/yolov3.cfg'
names_path   = './data/yolo3/coco.names'

image_path   = './test_samples/sample.jpg'
output_path  = './image/yolov3_result.jpg'

# 1) 클래스 이름 로드
with open(names_path, 'r', encoding='utf-8') as f:
    class_names = [line.strip() for line in f.readlines()]

# 2) YOLO 네트워크 불러오기
net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
# GPU 사용시:
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# 3) 이미지 읽기
img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError(f"이미지를 불러오지 못했습니다. 경로를 확인해주세요: {image_path}")
(h, w) = img.shape[:2]

# 4) blob 생성
blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)

# 5) YOLO가 사용할 출력 레이어명
ln = net.getUnconnectedOutLayersNames()
layer_outputs = net.forward(ln)

boxes = []
confidences = []
class_ids = []

# 6) 디텍션 결과 파싱
for output in layer_outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > 0.5:  # 임계값(Threshold)은 필요에 맞춰 조정
            box = detection[0:4] * np.array([w, h, w, h])
            (center_x, center_y, width_box, height_box) = box.astype(int)

            x = int(center_x - (width_box / 2))
            y = int(center_y - (height_box / 2))

            boxes.append([x, y, int(width_box), int(height_box)])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# 7) NMS(Non-Max Suppression)
idxs = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

# 8)   클래스별 색상 할당
#    - np.random.seed(...) 등으로 시드를 지정해두면 매번 동일하게 생성.
#    - 각 클래스마다 한 번 색상을 뽑은 후, 이미지에서 계속 동일 색으로 표현.
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(class_names), 3), dtype="uint8")

# 9) 박스 그리기
if len(idxs) > 0:
    for i in idxs.flatten():
        x, y, w_box, h_box = boxes[i]
        label = str(class_names[class_ids[i]])
        conf  = confidences[i]

        # 이 박스 클래스의 색상 (B, G, R)
        color = (int(colors[class_ids[i]][0]),
                 int(colors[class_ids[i]][1]),
                 int(colors[class_ids[i]][2]))

        cv2.rectangle(img, (x, y), (x + w_box, y + h_box), color, 2)
        text = f"{label}: {conf:.2f}"
        cv2.putText(img, text, (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

# 10) 이미지 저장
cv2.imwrite(output_path, img)
print("디텍트 결과 이미지를 저장했습니다:", output_path)

