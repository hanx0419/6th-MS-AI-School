import requests
import os
from dotenv import load_dotenv

load_dotenv()
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
azure_oai_key = os.getenv("AZURE_OAI_KEY")
azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
azure_search_key = os.getenv("AZURE_SEARCH_KEY")
azure_search_index = os.getenv("AZURE_SEARCH_INDEX")
azure_index_semantic = os.getenv("AZURE_INDEX_SEMANTIC")

def main(text):
    # header
    headers = {
        "Content-Type": "application/json",
        "api-key": azure_oai_key
    }

    # body
    body = {
            "messages": [
            {
                "role": "user",
                "content": text
            }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 800,
            "data_sources": [{
                "type": "azure_search",
                "parameters": {
                    "endpoint": azure_search_endpoint,
                    "index_name": azure_search_index,
                    "semantic_configuration": azure_index_semantic,
                    "query_type": "semantic",
                    "fields_mapping": {},
                    "in_scope": True,
                    "role_information": "You are a helpful travel agent",
                    "filter": None,
                    "strictness": 4,
                    "top_n_documents": 10,
                    "authentication": {
                    "type": "api_key",
                    "key": azure_search_key        
                            }
                            }
                            }
                            ]
}
    # POST 요청
    response = requests.post(azure_oai_endpoint, headers=headers, json=body)
    
    if response.status_code == 200:
        response_json = response.json()
        choices = response_json.get('choices', [])
        
        if not choices:
            print("No choices available.")
            return
        
        for idx, choice in enumerate(choices, 1):
            message = choice.get("message", {})
            answer_text = message.get("content", "")
            print(f"여행지{idx}:")
            print(answer_text)
            print("-" * 200)
            
            citations = message.get("context", {}).get("citations", [])
            if citations:
                for citation in citations:
                    print(citation.get("content", "No citation content"))
                    print("-" * 200)
            else:
                print("citation 정보가 없습니다.")
                print("-" * 200)
            print("-" * 200)
    else:
        print("Response is not 200")   
    
if __name__ == '__main__': 
    while True:
        text = input("질문을 입력하세요 (종료하려면 'quit' 입력): ")
        if text.strip().lower() == "quit":
            print("프로그램을 종료합니다.")
            break
        main(text)
