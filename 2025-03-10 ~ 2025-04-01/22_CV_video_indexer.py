import os
import requests
from dotenv import load_dotenv

load_dotenv()

# 환경 변수에서 중요한 설정값 불러오기
ENDPOINT = os.getenv("COMPUTER_VISION_ENDPOINT")
KEY = os.getenv("COMPUTER_VISION_KEY")
BLOB_SAS_URL = os.getenv("BLOB_SAS_URL")

INDEX_NAME = "MyVideoIndex"
INGESTION_NAME = "MyIngestion"


def create_index(endpoint: str, key: str, index_name: str) -> requests.Response:
    """Azure Video Retrieval 인덱스 생성."""
    url = f"{endpoint}computervision/retrieval/indexes/{index_name}?api-version=2023-05-01-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    payload = {
        "metadataSchema": {
            "fields": [
                {
                    "name": "cameraId",
                    "searchable": False,
                    "filterable": True,
                    "type": "string",
                },
                {
                    "name": "timestamp",
                    "searchable": False,
                    "filterable": True,
                    "type": "datetime",
                },
            ]
        },
        "features": [
            {"name": "vision", "domain": "surveillance"},
            {"name": "speech"},
        ],
    }

    return requests.put(url, headers=headers, json=payload)


def ingest_video(
    endpoint: str, key: str, index_name: str, ingestion_name: str, blob_sas_url: str
) -> requests.Response:
    """동영상(Blob) 파일을 인덱스에 등록."""
    url = f"{endpoint}computervision/retrieval/indexes/{index_name}/ingestions/{ingestion_name}?api-version=2023-05-01-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    payload = {
        "videos": [
            {
                "mode": "add",
                "documentId": "02a504c9cd28296a8b74394ed7488045",
                "documentUrl": blob_sas_url,
                "metadata": {
                    "cameraId": "camera1",
                    "timestamp": "2023-06-30 17:40:33",
                },
            }
        ]
    }

    return requests.put(url, headers=headers, json=payload)


def get_ingestions(endpoint: str, key: str, index_name: str, top: int = 20) -> requests.Response:
    """현재 진행 중인 Ingestion 목록 조회."""
    url = f"{endpoint}computervision/retrieval/indexes/{index_name}/ingestions?api-version=2023-05-01-preview&$top={top}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    return requests.get(url, headers=headers)


def query_by_text(
    endpoint: str, key: str, index_name: str, query_text: str
) -> requests.Response:
    """메타데이터와 함께 텍스트 검색."""
    url = f"{endpoint}computervision/retrieval/indexes/{index_name}:queryByText?api-version=2023-05-01-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    payload = {
        "queryText": query_text,
        "filters": {
            "stringFilters": [
                {
                    "fieldName": "cameraId",
                    "values": ["camera1"],
                }
            ],
            "featureFilters": ["speech", "vision"],
        },
    }

    return requests.post(url, headers=headers, json=payload)


def main():
    # 1. 인덱스 생성
    resp_create = create_index(ENDPOINT, KEY, INDEX_NAME)
    print(f"[인덱스 생성] {resp_create.status_code} => {resp_create.text}")

    # 2. 동영상 등록
    resp_ingest = ingest_video(ENDPOINT, KEY, INDEX_NAME, INGESTION_NAME, BLOB_SAS_URL)
    print(f"[동영상 등록] {resp_ingest.status_code} => {resp_ingest.text}")

    # 3. 수집 상태 조회 (수집 완료까지 주기적으로 확인 가능)
    resp_ingestions = get_ingestions(ENDPOINT, KEY, INDEX_NAME)
    print(f"[수집 상태 조회] {resp_ingestions.status_code} => {resp_ingestions.text}")

    # 4. 텍스트 검색
    resp_query = query_by_text(ENDPOINT, KEY, INDEX_NAME, "Microsoft")
    print(f"[검색 결과] {resp_query.status_code} => {resp_query.text}")


if __name__ == "__main__":
    main()