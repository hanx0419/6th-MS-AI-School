import os
from dotenv import load_dotenv
from openai import AzureOpenAI 

azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
azure_oai_key = os.getenv("AZURE_OAI_KEY")
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
azure_search_key = os.getenv("AZURE_SEARCH_KEY")
azure_search_index = os.getenv("AZURE_SEARCH_INDEX")


def main(): 
    try: 
        # Get configuration settings from .env file
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        
        # Validate configuration
        if not azure_oai_endpoint or not azure_oai_key or not azure_oai_deployment:
            raise ValueError("Missing one or more Azure OpenAI configuration settings.")

        # Initialize the Azure OpenAI client
        client = AzureOpenAI(
            api_key=azure_oai_key,
            api_version="2024-02-15-preview",  # 사용 중인 API 버전에 따라 조정
            azure_endpoint=azure_oai_endpoint
        )

        while True:
            # Get input text
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            print("\nSending request for summary to Azure OpenAI endpoint...\n\n")
            
            # Send request to Azure OpenAI
            try:
                response = client.chat.completions.create(
                    model=azure_oai_deployment,  # deployment name
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": input_text}
                    ],
                    temperature=0.7,
                    max_tokens=800
                )

                # Print the generated response  
                print("Response from Azure OpenAI:\n")
                print(response.choices[0].message.content)
                print("-" * 200)

            except Exception as api_ex:
                print("Error while calling Azure OpenAI:", api_ex)

    except Exception as ex:
        print("Fatal error:", ex)

if __name__ == '__main__': 
    main()