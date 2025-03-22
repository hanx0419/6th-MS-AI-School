import os
from dotenv import load_dotenv

load_dotenv()

language_key = os.getenv("AZURE_LANGUAGE_KEY")
language_endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=language_endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example method for summarizing text
def sample_extract_and_abstractive_summarization(client):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import (
        TextAnalyticsClient,
        ExtractiveSummaryAction,
        AbstractiveSummaryAction
    ) 

    document = [
       """
       전날 가격이 올랐던 비트코인이 다시 떨어졌다. 도널드 트럼프 미국 대통령이 친(親)가상화폐 정책을 통해 미국을 비트코인 초강대국이자 가상화폐의 수도로 만들겠다는 뜻을 거듭 강조했지만 비트코인 가격은 오히려 하락했다.

21일 오후 2시 코인게코 기준 비트코인 가격은 전날 같은 시간보다 1.7% 내린 8만4418달러를 기록했다. 비트코인은 전날 미국 연방준비제도(Fed·연준)의 연내 기준금리 인하에 대한 기대로 반등하며 8만7301달러까지 상승했으나 하루 만에 8만4000달러 선으로 주저앉았다.

트럼프 대통령은 20일(현지시간) 뉴욕에서 열린 가상자산 콘퍼런스에 사전 녹화한 영상 연설을 보내 이목을 끌었다. 트럼프 대통령은 “미국을 가상자산 수도로 만들고 가상자산과 차세대 금융 기술을 지배할 것”이라고 밝혔다. 이는 트럼프 대통령이 작년 대선 후보로 내세운 공약이기도 하다.

이어 트럼프 대통령은 “미국은 비트코인을 전략비축 자산에 포함했다”며 “정부는 보유 비트코인을 매각하지 않겠다”고 강조했다. 또 그는 “가상자산에 대한 불합리한 규제도 철폐하겠다”고 덧붙였다. 그러나 이날 나온 발언은 매번 해왔던 말에 불과해 시장 기대에는 미치지 못했다.

김병준 디스프레드 리서처는 “트럼프 대통령의 연설 이후 비트코인 가격이 오히려 하락한 현상은 친크립토 성향의 정치적 발언에 대한 시장 기대가 이미 가격에 반영돼 있음을 시사한다”고 설명했다. 이어 그는 “비트코인 가격은 앞으로 연준의 금리 인하 결정과 트럼프 정부의 관세 정책으로 인한 글로벌 국가들의 대응 등 거시경제적 요인들이 더 강한 영향력을 미칠 것”이라고 전망했다.

한편 트럼프 대통령은 이날 스테이블코인에 대한 발언도 쏟아냈다. 트럼프 대통령은 “달러화 기반 스테이블코인은 달러 지배력 강화에 도움 될 것”이라며 “의회에 스테이블코인 관련 법안 통과를 촉구했다”고 말했다.
       """
    ]

    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractiveSummaryAction(max_sentence_count=4),
            AbstractiveSummaryAction()
        ],
    )

    document_results = poller.result()
    for result in document_results:
        # Process Extractive Summary result (first action)
        extract_result = result[0]
        if extract_result.is_error:
            print("Extractive Summary Error: Code '{}' and message '{}'".format(
                extract_result.code, extract_result.message))
        else:
            print("=== Extractive Summary ===")
            for sentence in extract_result.sentences:
                # Print the sentence text
                print("Sentence:", sentence.text)
                # Print boundary details if available (e.g., offset and length)
                # Note: These properties depend on the service version; adjust as needed.
                if hasattr(sentence, 'offset') and hasattr(sentence, 'length'):
                    print("Boundary - Offset: {}, Length: {}".format(sentence.offset, sentence.length))
                print()  # For readability

        # 참고 Abstractive Summarization 기능이 영어 데이터셋에 기반한다는 점 
        # Process Abstractive Summary result (second action)
        abstractive_result = result[1]
        if abstractive_result.is_error:
            print("Abstractive Summary Error: Code '{}' and message '{}'".format(
                abstractive_result.code, abstractive_result.message))
        else:
            print("=== Abstractive Summary ===")
            for summary in abstractive_result.summaries:
                print(summary.text)
            print()

sample_extract_and_abstractive_summarization(client)