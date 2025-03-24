import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

def text_to_speech():
    # 환경변수 로드
    load_dotenv()
    speech_key = os.getenv('SPEECH_KEY')
    speech_region = "eastus2"

    # Speech SDK 설정 구성
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    # 필요한 경우, 음성의 스타일을 설정할 수 있습니다.
    # 예: speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    # 기본 스피커를 오디오 출력으로 사용하는 Speech Synthesizer 생성
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    text = """
            Hello, thank you for calling Contoso, who am I speaking with today? Hi, my name is Mary Rondo. 
            I'm trying to enroll myself with Contuso. Hi Mary. Uh, are you calling because you need health insurance? 
            Yes, Yeah, I'm calling to sign up for insurance. Great. Uh, if you can answer a few questions, uh, we can get you signed up in a jiffy. 
            OK, So, uh, what's your full name? Uh, so Mary Beth Rondo, last name is R like Romeo, O like ocean, N like Nancy, 
            DD like Dog, and O like Ocean again. Rondo got it. And what's the best callback number in case we get disconnected? 
            I only have a cell phone, so I can give you that. Yeah, that would be fine. Sure. So it's 234554 and then 9312. Got it. So to confirm, 
            it's 234-554-9312. Yep, that's right. Excellent. Let's get some additional information from your from your application. Do you have a job? Yes, 
            I am self-employed. OK, so then you have a Social Security number as well? Yes, I do. OK and what is your Social Security number please? 
            Sure. So it's 412256789. Sorry, what was that A25 or A225 you cut out for a bit? It's 22, so 412, then another two, then 5. 
            Alright, thank you so much. And could I have your e-mail address pleaseyeahitsmaryrondo@gmail.com? So myfirstandlastname@gmail.com. 
            No periods, no dashes. Great. That is the last question. So let me take your information and I'll be able to get you signed up right away. 
            Thank you for calling Contoso and I'll be able to get you signed up immediately. 
            One of our agents will call you back in about 24 hours or so to confirm your application. That sounds great. Thank you. Absolutely. 
            If you need anything else, please give us a call at 1-800-555-5564 ext 123. Uh, thank you very much for calling Contessa. Actually, 
            I have one more question. Yes, of course. I'm curious, will I be getting a physical card as proof of coverage? So the default is a digital membership card, 
            but we can send you a physical card if you prefer. Yes. Could you please mail it to me when it's ready? I'd like to have it shipped to umm, or my address. 
            Uh yeah. Uh, so it's 2660 Unit A on Maple Ave. SE, Lansing, and then zip code is 48823. Absolutely. I've made a note on your file. Awesome. Thanks so much. 
            You're very welcome. Thank you for calling Contoso and have a great day. 
           """
    print("Synthesizing speech for text: {}".format(text))

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized successfully!")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

if __name__ == "__main__":
    text_to_speech()