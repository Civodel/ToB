from openai import OpenAI

from src.config.const import DEEPSSEEK_API_KEY, PROMPT, PROMPT_REFINACION

# sclient = OpenAI(api_key=DEESEEK_API_KEY, base_url="https://api.deepseek.com")

DEESEEK_URL = "https://api.deepseek.com"

messages = []
postura_definida = False
postura_actual = ""

client = OpenAI(api_key=DEEPSSEEK_API_KEY, base_url=DEESEEK_URL)


def valid_user_input(user_message):
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        max_tokens=50,
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": user_message},
        ],
        stream=False
    )
    print(response.choices[0].message.content)

    input_usuario = response.choices[0].message.content
    if all(key in input_usuario for key in ['postura']):
        postura_definida = True
    else:
        postura_definida = False

    return postura_definida, input_usuario


def valid_final_response(pre_response):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": PROMPT_REFINACION},
            {"role": "user", "content": pre_response},
        ],
        stream=False
    )
    print(response.choices[0].message.content)

    return response.choices[0].message.content
