from openai import OpenAI
import json

def chat_output(apikey, MODEL_NAME, user_prompt):
    client = OpenAI(
        api_key=apikey,
        base_url="https://api.together.xyz/v1",
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """Give desired JSON equivalent for the statement given by the user. 
                      The two keys should be labeled as ledger_name and under_group""",
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        model=MODEL_NAME,
    )
    return chat_completion.choices[0].message.content

def extract_json_objects(text, decoder=json.JSONDecoder()):
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except json.JSONDecodeError as e:
            print("Error converting JSON string:", e)
            return None
        except ValueError:
            pos = match + 1

def json_extractor(text):
    for result in extract_json_objects(text):
        return result

