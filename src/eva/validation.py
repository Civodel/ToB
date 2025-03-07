import openai
from openai import OpenAI

from src.config.const import PROMPT, DEEPSSEEK_API_KEY, DEESEEK_URL, PROMPT_REFINACION

openai.api_key = DEEPSSEEK_API_KEY
openai.api_base = DEESEEK_URL

client = OpenAI(api_key=DEEPSSEEK_API_KEY, base_url=DEESEEK_URL)


def valid_user_input(user_message: str) -> list:
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            max_tokens=20,
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": user_message},
            ],
            stream=False,
            temperature=0.7,
            top_p=1,
        )
        print(response.choices[0].message.content)

        input_usuario = response.choices[0].message.content

        if 'postura' in input_usuario:
            return [True, input_usuario]

        return [False, input_usuario]
    except Exception as e:
        print("Error:", e)
        return [False, "Ocurrió un error. Intenta de nuevo."]


def valid_final_response(pre_response, user_message):
    refined_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": PROMPT_REFINACION.format(respuesta_original=pre_response)}
        ],
        max_tokens=100,  # Prueba con menos tokens
        temperature=0.7,
        top_p=0.95,
        stream=False,

    )

    return refined_response.choices[0].message.content
