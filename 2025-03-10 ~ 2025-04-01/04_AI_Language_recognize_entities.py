import os
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

language_key = os.getenv("AZURE_LANGUAGE_KEY")
language_endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")


# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=language_endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example function for recognizing entities from text
def entity_recognition_example(client):

    try:
        documents = [
            """
            21일 한국거래소에 따르면 이날 코스피 지수는 전장 대비 0.23% 오른 2643.13에 거래를 마쳤다. 
            전장 대비 0.12% 내린 2633.90에 출발한 코스피 지수는 오전 중 상승 전환에 성공하더니 마지막까지 상승분을 지켜내며 강보합 마감했다.
            유가증권시장에서는 외국인이 8512억원어치를 순매수했다. 외국인이 하루만에 8000억원 넘게 순매수에 나선 건 지난해 8월 이후 처음이다. 
            특히 외국인은 지난 17일부터 이날까지 5거래일 연속 순매수를 이어갔다. 반면 이날 개인과 기관은 각각 5407억원, 4000억원어치를 팔아치웠다.
            """
        ]
        result = client.recognize_entities(documents = documents)[0]

        print("Named Entities:\n")
        for entity in result.entities:
            print("\tText: \t", entity.text, "\tCategory: \t", entity.category, "\tSubCategory: \t", entity.subcategory,
                    "\n\tConfidence Score: \t", round(entity.confidence_score, 2), "\tLength: \t", entity.length, "\tOffset: \t", entity.offset, "\n")

    except Exception as err:
        print("Encountered exception. {}".format(err))
entity_recognition_example(client)