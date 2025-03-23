import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

load_dotenv()

endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")
knowledge_base_project = os.getenv("CUSTOM_QUESTION_ANSWERING_PROJECT_NAME")
credential = AzureKeyCredential(key)
deployment = "production"

def main():
    client = QuestionAnsweringClient(endpoint, credential)
    with client:
        question="How do i setup my surface book?"
        output = client.get_answers(
            question = question,
            project_name=knowledge_base_project,
            deployment_name=deployment
        )
    print("Q: {}".format(question))
    print("A: {}".format(output.answers[0].answer))

if __name__ == '__main__':
    main()