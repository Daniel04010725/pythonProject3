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

API_KEY = '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'
openai.api_key = API_KEY


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
            chat_history += f'User: {user_message}<br>User(eng): {translate_text_return}<br>Chatbot(eng): {resulttext.content}<br>Chatbot: {chatbot_message}<br>'
            # chat_history += f'User: {user_message}<br>Chatbot: {chatbot_message}<br>'
            user_message = ''
    else:
        chat_history = ''

    return render(request, 'chat/post_list.html', {'chat_history': chat_history})


