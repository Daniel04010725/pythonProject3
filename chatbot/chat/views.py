from __future__ import division

'''
from django.http import HttpResponse

from django.shortcuts import render

def post(request):
    if request.method == 'POST':
        return render(request, 'post_list.html', {'POST':'POST방식입니다!!'})



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
'''
# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render
# from .models import Question
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# 구글 API
import sys
# Imports the Google Cloud Translation library
from google.cloud import translate

# Open API
import os
import openai

# stt를 위한 API 호출
##from . import stt


openai.api_key = os.getenv("OPENAI_API_KEY")


# 구글 번역 함수 선언
# Initialize Translation client
def translate_text1(text):
    """Translating Text."""

    client = translate.TranslationServiceClient()
    project_id = "mintpot-test"

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from English to French
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "ko",
            "target_language_code": "en-US",
        }
    )
    # Display the translation for each input text provided
    for translation in response.translations:
        global translate_text_return
        translate_text_return = translation.translated_text
        print("Translated text: {}".format(translate_text_return))


def translate_text2(text):
    """Translating Text."""

    client = translate.TranslationServiceClient()
    project_id = "mintpot-test"

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from English to French
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "en-US",
            "target_language_code": "ko",
        }
    )
    # Display the translation for each input text provided
    for translation in response.translations:
        global translate_text_return2
        translate_text_return2 = translation.translated_text
        print('''

       '''"Translated text(Eng->Ko): {}".format(translate_text_return2))


# open api 함수선언
def f1(user_message):
    prompt = user_message
    print(prompt)

    translate_text1(prompt)

    '''
    response = openai.Completion.create(
        prompt = translate_text_return,
        model = 'text-davinci-003',
        max_tokens=1000,
        temperature=0.9,
        n=1,
        stop=['---']
    )


    #print(response)
    #print(response.usage.total_tokens)

    for result in response.choices:
        global resulttext
        resulttext = result.text
        print("AI(ENG): {}".format(result.text))
        translate_text2(result.text)
        r= translate_text_return2
        print(r)
        return r
    '''

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": translate_text_return}
        ]
    )
    print(response.choices[0].message.content)

    # print(response)
    # print(response.usage.total_tokens)

    for result in response.choices:
        global resulttext
        resulttext = response.choices[0].message
        print("AI(ENG): {}".format(resulttext))
        translate_text2(resulttext.content)
        r = translate_text_return2
        print(r)
        return r


# post_list 접속하면 아래 함수 실행, 챗봇에서 데이터 받아와서 리턴해주기
def post_list(request):
    #요청이 post인경우 아래 실행
    if request.method == 'POST':
        user_message = request.POST.get('user_message')
        if user_message == '':
            chat_history = ''
        else:
            print(user_message)
            chatbot_message = f1(user_message)
            print(chatbot_message)
            # 번역 및 AI 함수 호출, 챗봇 로직을 수행하여 응답 메시지 생성
            # chatbot_message = test.f1(user_message)

            #        # 챗봇 로직을 수행하여 응답 메시지 생성
            # chatbot_message = "챗봇 응답 메시지2"

            # 현재까지 대화 내용을 누적하여 전달
            chat_history = request.POST.get('chat_history')
            #영어 답변 넣어서
            chat_history += f'User: {user_message}<br>User(eng): {translate_text_return}<br>Chatbot(eng): {resulttext.content}<br>Chatbot: {chatbot_message}<br>'
            #영어 답변 없이는 아래것으로
            #chat_history += f'User: {user_message}<br>Chatbot: {chatbot_message}<br>'

            user_message = ''
    else:
        chat_history = ''

    return render(request, 'chat/post_list.html', {'chat_history': chat_history})



#eng_stt 요청올때
def eng_stt(request):
    #요청이 post인경우 아래 실행
    if request.method == 'POST':
        user_message = "안녕하세요"
        print(main())
        user_message = transcript_history

        if user_message == '':
            chat_history = ''
        else:
            print(user_message)
            chatbot_message = f1(user_message)
            print(chatbot_message)

            # 현재까지 대화 내용을 누적하여 전달
            chat_history = request.POST.get('chat_history')

            #영어 답변 없이는 아래것으로
            chat_history += f'User: {user_message}<br>Chatbot: {resulttext.content}<br>'

            user_message = ''
    else:
        chat_history = ''

    return render(request, 'chat/eng_stt.html', {'chat_history': chat_history})

















import re
import sys

from google.cloud import speech

import pyaudio
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    # 글로벌로 변수지정
    global transcript
    global transcript_history
    transcript_history = ""

    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue
        



        # Display the transcription of the top alternative.
        # 최상위 대안의 전사를 표시합니다.
        transcript = result.alternatives[0].transcript


        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        # 중간 결과를 표시하지만 끝에 캐리지 리턴이 있습니다.
        # 줄이므로 후속 줄이 덮어씁니다.
        #
        # 이전 결과가 이것보다 길면 인쇄해야 합니다.
        # 이전 결과를 덮어쓸 여분의 공백


        overwrite_chars = " " * (num_chars_printed - len(transcript))

        #여러번 덮어씌우는것 \r이 덮어씌우는것의 줄바꿈 아니다
        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        #여기가 입력 제대로 받는곳
        else:
            print(transcript + overwrite_chars)
            
            # #계속 더하기
            # transcript_history += transcript

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            # 필사된 문구가 있을 수 있는 경우 종료 인식
            # 키워드 중 하나.
            #음성 입력으로 종료 인식
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break

                # 계속 더하기
            else:
                transcript_history += transcript

            num_chars_printed = 0


def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = "en-US"  # a BCP-47 language tag
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)

if __name__ == "__main__":
    main()