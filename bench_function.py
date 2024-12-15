## python bench_main.py --model ./model_test --eval_api groq --eval_model "llama3-70b-8192" --bench_mark ./test.jsonl

import argparse
import os
import json

from auto_bench.funs import *

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def bench_func(model_name,eval_api,eval_model,bench_mark_path):
    tokenizer_name = ""

    if tokenizer_name == "":
        tokenizer_name = model_name

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16, device_map="auto")

    def local_LLM(user_input):
        messages = [
            {"role": "user", "content": user_input},
        ]
        input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(model.device)

        outputs = model.generate(
            input_ids,
            do_sample=True,
            temperature=0.2, ## Recommend 0.6 or lower
            max_new_tokens=1024
        )
        response = outputs[0][input_ids.shape[-1]:]
        return tokenizer.decode(response, skip_special_tokens=True)

    bench_mark_data = read_file(bench_mark_path)
    count = 0 
    score = []

    for data in bench_mark_data:
        local_LLM_answer = local_LLM(data["input"])
        # print(f"問題: {data['input']}")
        res = integration_chat(
            """
    問題, 正解例, 採点基準, 言語モデルが生成した回答が与えられます。

    # 指示
    「採点基準」と「正解例」を参考にして、回答を1,2,3,4,5の5段階で採点し、数字のみを出力してください。

    # 問題
    """
                    + str(data["input"])
                    + """

    # 正解例
    """
                    + str(data["output"])
                    + """

    # 採点基準
    基本的な採点基準
    - 1点: 誤っている、 指示に従えていない
    - 2点: 誤っているが、方向性は合っている
    - 3点: 部分的に誤っている、 部分的に合っている
    - 4点: 合っている
    - 5点: 役に立つ

    基本的な減点項目
    - 不自然な日本語: -1点
    - 部分的に事実と異なる内容を述べている: -1点
    - 「倫理的に答えられません」のように過度に安全性を気にしてしまっている: 2点にする

    問題固有の採点基準
    """
                    + str(data["eval_aspect"])
                    + """

    # 言語モデルの回答
    """
                    + str(local_LLM_answer)
                    + """

    # ここまでが'言語モデルの回答'です。回答が空白だった場合、1点にしてください。

    # 指示
    「採点基準」と「正解例」を参考にして、回答を1,2,3,4,5の5段階で採点し、数字のみを出力してください。
            ""","あなたは優秀な採点者エージェントです。出力は数字のみでおねがいします。",eval_api,eval_model)
        # print("得点"+res)
        count += 1
        # print(count)
        with open(model_name+"/result.jsonl", "a", encoding="utf-8") as f:
            json_str = json.dumps(
                {
                    "input": data["input"],
                    "output": local_LLM_answer,
                    "eval_aspect": data["eval_aspect"],
                    "score": res
                },
                ensure_ascii=False
            )
            f.write(json_str + "\n")

        score.append(int(res))

    models_score = sum(score) / len(score)

    print(models_score)
    return models_score