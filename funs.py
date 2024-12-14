import openai
from groq import Groq

import os
import json

from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

SYSTEM_PROMPT = "あなたは優秀な日本語AIです。原則的に日本語で回答してください。"

SYSTEM_PROMPT = "あなたは優秀な日本語AIです。原則的に日本語で回答してください。"
IMG_SYSTEM_PROMPT = "あなたは優秀な日本語AIです。原則的に日本語で回答してください。"

client_groq = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
    )
client_ollama = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # required, but unused
)
client_llamacpp = openai.OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="any_thing",  # required, but unused
)
client_xai = openai.OpenAI(
    api_key=os.environ.get("XAI_API_KEY"), base_url="https://api.x.ai/v1"
)

def ollama_chat(user_inputs, system_prompt=SYSTEM_PROMPT, main_model="qwen2.5:latest"):
    input_messages_list = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_inputs},
    ]
    completion = client_ollama.chat.completions.create(
        model=main_model, messages=input_messages_list
    )
    return completion.choices[0].message.content

def llamacpp_chat(
    user_inputs, system_prompt=SYSTEM_PROMPT, main_model="gemma2:9b-instruct-q4_K_M"
):
    input_messages_list = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_inputs},
    ]
    completion = client_llamacpp.chat.completions.create(
        model=main_model, messages=input_messages_list
    )
    return completion.choices[0].message.content

def groq_chat(
    user_inputs, system_prompt=SYSTEM_PROMPT, main_model="gemma2-9b-it"
):
    input_messages_list = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_inputs},
    ]
    completion = client_groq.chat.completions.create(
        messages=input_messages_list, model=main_model
    )
    return completion.choices[0].message.content

def xai_chat(user_inputs, system_prompt=SYSTEM_PROMPT, main_model="grok-beta"):
    input_messages_list = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_inputs},
    ]
    completion = client_xai.chat.completions.create(
        model=main_model, messages=input_messages_list
    )
    return completion.choices[0].message.content

def integration_chat(user_inputs, system_prompt=SYSTEM_PROMPT, API="groq", model = "gemma2-9b-it"):
    if API == "groq":
        return groq_chat(user_inputs, system_prompt, model)
    elif API == "ollama":
        return ollama_chat(user_inputs, system_prompt, model)
    elif API == "llamacpp":
        return llamacpp_chat(user_inputs, system_prompt, model)
    elif API == "xai":
        return xai_chat(user_inputs, system_prompt, model)
    else:
        print("Error: Invalid API")
        return None

def read_file(file_path):
    """
    指定されたファイルパスを読み込み、ファイルの種類に応じて適切なデータ形式を返す関数

    Args:
      file_path (str): ファイルのパス

    Returns:
      Union[str, list]: テキストファイルの場合は文字列、JSONファイルまたはJSONLファイルの場合はリスト（辞書型）
    """

    if file_path.endswith(".txt"):
        with open(file_path, "r") as f:
            return f.read()
    elif file_path.endswith((".json", ".jsonl")):
        with open(file_path, "r") as f:
            if file_path.endswith(".json"):
                return json.load(f)
            else:  # .jsonlの場合
                return [json.loads(line) for line in f]
    else:
        with open(file_path, "r") as f:
            return f.read()