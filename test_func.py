
#def test_f1(p):
#    print("함수진행")
#    p = p + 10
#    print(p)
#    return p


import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

def f1(user_message):
    prompt = user_message
    print("func: {}".format(prompt))

    response = openai.Completion.create(
        prompt = prompt,
        model = 'text-davinci-003',
        max_tokens=1000,
        temperature=0.9,
        n=1,
        stop=['---']
    )
    #print(response)
    #print(response.usage.total_tokens)
    for result in response.choices:
        r= result.text
        print("func: {}".format(r))
        return r

#user_message="한국 여자아이 이름 추천"
#print(user_message)
#chatbot_message = f1(user_message)
#print(chatbot_message)