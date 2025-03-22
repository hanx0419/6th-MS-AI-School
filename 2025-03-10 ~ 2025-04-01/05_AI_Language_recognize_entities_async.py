import asyncio


async def sample_recognize_entities_async() -> None:
    print(
        "In this sample, we are a catering business, and we're looking to sort the reviews "
        "for our organization based off of the organization that hired us for catering"
    )

    # [START recognize_entities_async]
    import os
    import typing
    from dotenv import load_dotenv
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics.aio import TextAnalyticsClient

    load_dotenv()

    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")

    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    reviews = [
        """I work for Foo Company, and we hired Contoso for our annual founding ceremony. The food
        was amazing and we all can't say enough good words about the quality and the level of service.""",
        """We at the Foo Company re-hired Contoso after all of our past successes with the company.
        Though the food was still great, I feel there has been a quality drop since their last time
        catering for us. Is anyone else running into the same problem?""",
        """Bar Company is over the moon about the service we received from Contoso, the best sliders ever!!!!"""
    ]
    ### Mission : 해당 부분 수정 #######################################################
    # async with text_analytics_client:
    #    result = await text_analytics_client.recognize_entities(reviews)
    # 전체 리뷰 목록을 한 번에 API에 전달하여 한 번의 비동기 호출로 처리
    # API에서 전체 리뷰에 대한 응답을 반환할 때까지 기다린 후, 결과를 단일 변수로 받아옵니다.

    # Asychronous call 발생
    # 이부분을 수정해서 reviews를 나눠서 여러번 호출하는 방법을 생각
    # 새로 생성하는 함수내에서 gather 함수 사용
    ####################################################################################

    async with text_analytics_client:
        async def process_review(review: str):
            # 각 호출은 단일 리뷰에 대해 리스트 형태로 호출합니다.
            return await text_analytics_client.recognize_entities([review])
        
        # 각 리뷰별 테스크 생성
        tasks = [asyncio.create_task(process_review(review)) for review in reviews]
        # 모든 테스크를 동시에 실행하고 결과를 받습니다.
        results_chunks = await asyncio.gather(*tasks)
        # 각 테스크의 결과는 단일 리뷰에 대한 리스트이므로, 이를 평탄화합니다.
        result = [item for sublist in results_chunks for item in sublist]
   
   # 개별 호출 후 동시 실행
   # 각 리뷰를 개별 리스트로 만들어 별도의 호출로 처리합니다
   # asyncio.create_task를 이용해 각 리뷰에 대해 독립적인 비동기 작업을 생성한 후, 
   # asyncio.gather를 통해 동시에 실행하여 모든 결과를 한 번에 모읍니다.
   #######################################################################################
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
    # [END recognize_entities_async]


async def main():
    await sample_recognize_entities_async()


if __name__ == '__main__':
    asyncio.run(main())
