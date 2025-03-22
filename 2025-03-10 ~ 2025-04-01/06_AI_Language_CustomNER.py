def sample_recognize_custom_entities() -> None:
    # [START recognize_custom_entities]
    import os
    from dotenv import load_dotenv
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    load_dotenv()

    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")
    project_name = os.getenv("CUSTOM_ENTITIES_PROJECT_NAME")
    deployment_name = os.getenv("CUSTOM_ENTITIES_DEPLOYMENT_NAME")

    path_to_sample_document = os.path.join(os.getcwd(), "text_samples", "custom_entities_sample.txt")

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    with open(path_to_sample_document) as fd:
        document = [fd.read()]

    poller = text_analytics_client.begin_recognize_custom_entities(
        document,
        project_name=project_name,
        deployment_name=deployment_name
    )

    document_results = poller.result()
    for custom_entities_result in document_results:
        if custom_entities_result.kind == "CustomEntityRecognition":
            for entity in custom_entities_result.entities:
                print(
                    "Entity '{}' has category '{}' with confidence score of '{}'".format(
                        entity.text, entity.category, entity.confidence_score
                    )
                )
        elif custom_entities_result.is_error is True:
            print("...Is an error with code '{}' and message '{}'".format(
                custom_entities_result.error.code, custom_entities_result.error.message
                )
            )
    # [END recognize_custom_entities]


if __name__ == "__main__":
    sample_recognize_custom_entities()