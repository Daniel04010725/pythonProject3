import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt= "한국 여자아이 이름 추천"

response = openai.Completion.create(
    prompt = prompt,
    model = 'text-davinci-003',
    max_tokens=1000,
    temperature=0.9,
    n=3,
    stop=['---']
)
#print(response)
#print(response.usage.total_tokens)
for result in response.choices:
    print(result.text)


print(os.getenv("OPENAI_API_KEY"))
