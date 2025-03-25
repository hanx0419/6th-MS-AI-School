def sample_classify_document_single_label() -> None:
    # [START single_label_classify]
    import os
    from dotenv import load_dotenv
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    load_dotenv()

    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")
    project_name = os.getenv("SINGLE_LABEL_CLASSIFY_PROJECT_NAME")
    deployment_name = os.getenv("SINGLE_LABEL_CLASSIFY_DEPLOYMENT_NAME")
    
    path_to_sample_document = os.path.join(os.getcwd(), "test_samples", "custom_classify_sample.txt")

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    with open(path_to_sample_document) as fd:
        document = [fd.read()]

    poller = text_analytics_client.begin_single_label_classify(
        document,
        project_name=project_name,
        deployment_name=deployment_name
    )

    document_results = poller.result()
    for doc, classification_result in zip(document, document_results):
        if classification_result.kind == "CustomDocumentClassification":
            classification = classification_result.classifications[0]
            print("The document text '{}' was classified as '{}' with confidence score {}.".format(
                doc, classification.category, classification.confidence_score)
            )
        elif classification_result.is_error is True:
            print("Document text '{}' has an error with code '{}' and message '{}'".format(
                doc, classification_result.error.code, classification_result.error.message
            ))
    # [END single_label_classify]


if __name__ == "__main__":
    sample_classify_document_single_label()