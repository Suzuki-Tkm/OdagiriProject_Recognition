import openai
import os

# OpenAI GPT-3のAPIキーを設定
openai.api_key = os.environ.get('API_KEY')

def generate_associated_words(color):
    # GPT-3に色に関連するワードを生成するためのプロンプトを送信
    prompt = f"Generate three words associated with the color {color}."
    response = openai.Completion.create(
        engine="text-davinci-002",  # 使用するエンジンを選択
        prompt=prompt,
        max_tokens=50,  # 生成されるテキストの最大トークン数
        n=1  # 生成するワードの数を1に変更
    )

    # APIの応答から生成されたワードを抽出
    generated_text = response['choices'][0]['text'].strip()

    return generated_text

# 例: 赤色に関連する3つのワードを取得
if __name__ == "__main__":
    color = "red"
    associated_words = generate_associated_words(color)
    print(associated_words)