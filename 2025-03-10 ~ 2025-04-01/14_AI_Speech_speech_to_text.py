import os
from dotenv import load_dotenv
import time
import azure.cognitiveservices.speech as speechsdk

def recognize_from_file_continuous():
    # 환경변수 로드
    load_dotenv()

    # Speech SDK 설정 구성
    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv('SPEECH_KEY'),
        region="eastus2"
    )
    speech_config.speech_recognition_language = "en-US"

    # 오디오 파일 경로 지정
    audio_config = speechsdk.audio.AudioConfig(
        filename="./text_samples/Call1_separated_16k_health_insurance.wav"
    )
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    # 종료 플래그
    done = False

    # 인식 결과 이벤트 핸들러
    def recognized_handler(evt):
        print("Recognized: {}".format(evt.result.text))

    # 세션 종료 및 취소 이벤트 핸들러
    def stop_handler(evt):
        nonlocal done
        done = True
        print("Session stopped or canceled: {}".format(evt))

    # 이벤트 연결
    speech_recognizer.recognized.connect(recognized_handler)
    speech_recognizer.session_stopped.connect(stop_handler)
    speech_recognizer.canceled.connect(stop_handler)

    # 연속 인식 시작
    print("Continuous recognition started. Processing audio file...")
    speech_recognizer.start_continuous_recognition()

    # 오디오 파일 처리가 완료될 때까지 대기
    while not done:
        time.sleep(0.5)

    speech_recognizer.stop_continuous_recognition()
    print("Recognition stopped.")

if __name__ == "__main__":
    recognize_from_file_continuous()
