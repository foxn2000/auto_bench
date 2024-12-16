# AUTO BENCH

このディレクトリには、言語モデルの自動ベンチマークを行うためのスクリプトが含まれています。

## ファイル構成

-   `.env`: 環境変数を設定するためのファイルです。
    -   `GROQ_API_KEY`: Groq API の API キーを設定します。
    -   `XAI_API_KEY`: X.ai API の API キーを設定します。
-   `.gitignore`: Git で無視するファイルを指定します。
-   `bench_function.py`: ベンチマークを実行するための関数を定義します。
-   `bench_main.py`: ベンチマークスクリプトのエントリーポイントです。コマンドライン引数を受け取り、ベンチマークを実行します。
-   `funs.py`: 各種APIとの連携やファイル読み込みなどの共通関数を定義します。
-   `requirements.txt`: 必要な Python パッケージをリストします。
-   `test.jsonl`: ベンチマークに使用する JSONL 形式のデータファイルです。

## スクリプトの説明

### `bench_function.py`

このファイルには、`bench_func` という関数が定義されています。この関数は、指定されたモデル、評価 API、評価モデル、ベンチマークデータを使用して、言語モデルのベンチマークを行います。

### `bench_main.py`

このファイルは、ベンチマークスクリプトのエントリーポイントです。コマンドライン引数でモデルのパス、評価 API、評価モデル、ベンチマークデータのパスを指定できます。

### `funs.py`

このファイルには、各種APIとの連携やファイル読み込みなどの共通関数が定義されています。

-   `ollama_chat`: Ollama API を使用してチャットを行う関数。
-   `llamacpp_chat`: llama.cpp API を使用してチャットを行う関数。
-   `groq_chat`: Groq API を使用してチャットを行う関数。
-   `xai_chat`: X.ai API を使用してチャットを行う関数。
-   `integration_chat`: 指定された API に基づいてチャットを行う関数。
-   `read_file`: ファイルを読み込み、ファイルの種類に応じて適切なデータ形式を返す関数。

## 環境変数

このスクリプトを実行するには、以下の環境変数が必要です。

-   `GROQ_API_KEY`: Groq API の API キー
-   `XAI_API_KEY`: X.ai API の API キー

これらの環境変数は、`.env` ファイルに設定する必要があります。

## 依存関係

このスクリプトを実行するには、以下の Python パッケージが必要です。

```
openai
groq
python-dotenv
transformers
torch
```

これらのパッケージは、`requirements.txt` ファイルにリストされています。以下のコマンドでインストールできます。

```bash
pip install -r requirements.txt
```

## 使用方法

`bench_main.py` スクリプトは、以下のコマンドで実行できます。

```bash
python bench_main.py --model <モデルのパス> --eval_api <評価API> --eval_model <評価モデル> --bench_mark <ベンチマークデータのパス>
```

-   `--model`: ベンチマーク対象のモデルのパスを指定します。
-   `--eval_api`: 使用する評価 API を指定します（例: `groq`, `ollama`, `llamacpp`, `xai`）。
-   `--eval_model`: 使用する評価モデルを指定します。
-   `--bench_mark`: ベンチマークデータのパスを指定します。

例：

```bash
python bench_main.py --model ./model_test --eval_api groq --eval_model "llama3-70b-8192" --bench_mark ./test.jsonl
```

## ベンチマークデータの形式

`test.jsonl` ファイルは、JSONL 形式で記述されたベンチマークデータです。各行は、以下のキーを持つ JSON オブジェクトです。

-   `input`: モデルへの入力テキスト。
-   `output`: 正解例。
-   `eval_aspect`: 採点基準。

## 注意点

-   APIキーは、`.env`ファイルに設定してください。
-   `bench_main.py`を実行する前に、必要なPythonパッケージをインストールしてください。
