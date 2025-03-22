def sample_recognize_entities() -> None:
    print(
        "In this sample, we are a catering business, and we're looking to sort the reviews "
        "for our organization based off of the organization that hired us for catering"
        # 인식된 엔터티의 카테고리를 모두 확인할 수 있지만, 최종적으로 리뷰를 정리하는 목적은 회사명을 기준으로 한 그룹화를 위한 것
    )

    # [START recognize_entities]
    import os
    import typing
    from dotenv import load_dotenv
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    load_dotenv()

    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")

    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    reviews = [
            """
            21일 한국거래소에 따르면 이날 코스피 지수는 전장 대비 0.23% 오른 2643.13에 거래를 마쳤다. 
            전장 대비 0.12% 내린 2633.90에 출발한 코스피 지수는 오전 중 상승 전환에 성공하더니 마지막까지 상승분을 지켜내며 강보합 마감했다.
            유가증권시장에서는 외국인이 8512억원어치를 순매수했다. 외국인이 하루만에 8000억원 넘게 순매수에 나선 건 지난해 8월 이후 처음이다. 
            특히 외국인은 지난 17일부터 이날까지 5거래일 연속 순매수를 이어갔다. 반면 이날 개인과 기관은 각각 5407억원, 4000억원어치를 팔아치웠다.
            """
    ]

    result = text_analytics_client.recognize_entities(reviews)
    result = [review for review in result if not review.is_error]
    organization_to_reviews: typing.Dict[str, typing.List[str]] = {}

    for idx, review in enumerate(result):
        for entity in review.entities:
            print(f"Entity '{entity.text}' has category '{entity.category}'")
            if entity.category == 'Organization':
                organization_to_reviews.setdefault(entity.text, [])
                organization_to_reviews[entity.text].append(reviews[idx])

    for organization, reviews in organization_to_reviews.items():
        print(
            "\n\nOrganization '{}' has left us the following review(s): {}".format(
                organization, "\n\n".join(reviews)
            )
        )
    # [END recognize_entities]


if __name__ == '__main__':
    sample_recognize_entities()