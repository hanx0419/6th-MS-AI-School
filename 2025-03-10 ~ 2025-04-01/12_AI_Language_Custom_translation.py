import requests, uuid, json
import os
from dotenv import load_dotenv

load_dotenv()

# 자신의 번역 리소스 속성에서 확인한 Subscription Key, Region
subscription_key = os.getenv("CUSTOM_TRANSLATION_KEY")
endpoint = "https://api.cognitive.microsofttranslator.com"  # 글로벌 엔드포인트
region = "southcentralus" 
category_id = os.getenv("CUSTOM_TRANSLATOR_MODEL_ID")

path = '/translate'
constructed_url = endpoint + path

# Custom Translator 모델을 지정하기 위한 파라미터: category=모델 ID
params = {
    'api-version': '3.0',
    'from': 'en',
    'to': 'ko',
    'category': category_id
}

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': region,  # 일부 지역/엔드포인트 조합에서 필수
    'Content-Type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

body = [{
    "text" : "Through computerized cognitive rehabilitation, cognitive function was significantly improved in patients with mild cognitive impairment and Alzheimer's disease."
}]

try:
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    
    translated_text = response[0]['translations'][0]['text']
    print(translated_text)
except Exception as e:
    print(e)