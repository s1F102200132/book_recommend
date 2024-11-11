# diary/utils.py
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from deep_translator import GoogleTranslator
import requests
from bs4 import BeautifulSoup

# モデルとトークナイザーの設定
model_name = "monologg/bert-base-cased-goemotions-original"  # 感情分析モデル
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# GoEmotionsのラベルリスト（日本語対応版）
goemotions_labels = [
    "賞賛", "楽しさ", "怒り", "苛立ち", "承認", "思いやり", 
    "混乱", "好奇心", "欲求", "失望", "不承認", 
    "嫌悪", "恥ずかしさ", "興奮", "恐怖", "感謝", "悲しみ", 
    "喜び", "愛", "緊張", "楽観", "誇り", "気づき", 
    "安心", "後悔", "悲しさ", "驚き", "中立"
]

# 翻訳用の初期化
translator = GoogleTranslator(source='ja', target='en')

def analyze_sentiment(text):
    try:
        # テキストを翻訳
        translated_text = translator.translate(text)
        print(f"翻訳文: {translated_text}")
    except Exception as e:
        print(f"翻訳中にエラーが発生しました: {e}")
        return None, 0  # エラーの場合はNoneと0を返す

    # テキストのトークナイズ
    inputs = tokenizer(translated_text, return_tensors="pt")
    
    # モデルを推論モードに設定
    with torch.no_grad():
        logits = model(**inputs).logits

    # ソフトマックス関数を使って確信度を計算
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    sentiment = torch.argmax(probabilities).item()
    confidence = probabilities[0][sentiment].item()

    # 日本語感情ラベルの取得
    label = goemotions_labels[sentiment]

    return label, confidence

def get_amazon_reviews(book_title):
    # 実際のAmazonのレビューを取得する（簡略化版）
    reviews = [
        {"book_title": "幸せになる勇気", "review": "小さなことから幸せを見つける方法を教えてくれる本です。"},
        {"book_title": "死ぬ瞬間の10のこと", "review": "生と死について深く考えさせられる一冊です。"},
        {"book_title": "恐れを感じても、前に進める勇気をくれる本", "review": "恐怖を乗り越える力を与えてくれる本です。"},
        {"book_title": "5つの愛の言語", "review": "人間関係を改善するためのヒントが詰まった本です。"},
        {"book_title": "嫌われる勇気", "review": "他人の期待に縛られず、自分らしく生きるためのヒントが詰まっています。"},
        {"book_title": "心の整理術", "review": "日常のストレスを軽減するためのシンプルな方法が学べる本です。"},
        {"book_title": "人を動かす", "review": "人間関係をより良くするためのコミュニケーション術が学べます。"},
        {"book_title": "内向型のあなたが才能を活かす方法", "review": "内向的な自分を肯定し、強みを活かす方法を示してくれます。"},
        {"book_title": "世界一やさしい「やる気」の言葉", "review": "モチベーションを高めるための優しい言葉が集められています。"},
        {"book_title": "引き寄せの法則", "review": "自分の思考が現実を作り出すという理論に基づいた本です。"},
        {"book_title": "スティーブ・ジョブズ 驚異のプレゼン", "review": "熱い情熱と集中力で成果を出す方法を学べる本です。"},
        {"book_title": "GRIT: やり抜く力", "review": "情熱と粘り強さが成功の鍵であることを教えてくれる本です。"},
        {"book_title": "モチベーション3.0", "review": "内発的動機づけを高めるための方法が学べます。"}
    ]
    # 実際のレビュー検索の部分（簡略化版）
    return [review for review in reviews if review["book_title"] == book_title]

def recommend_book_by_sentiment(diary_sentiment):
    reviews = [
        {"book_title": "幸せになる勇気", "review": "小さなことから幸せを見つける方法を教えてくれる本です。"},
        {"book_title": "死ぬ瞬間の10のこと", "review": "生と死について深く考えさせられる一冊です。"},
        {"book_title": "恐れを感じても、前に進める勇気をくれる本", "review": "恐怖を乗り越える力を与えてくれる本です。"},
        {"book_title": "5つの愛の言語", "review": "人間関係を改善するためのヒントが詰まった本です。"},
        {"book_title": "嫌われる勇気", "review": "他人の期待に縛られず、自分らしく生きるためのヒントが詰まっています。"},
        {"book_title": "心の整理術", "review": "日常のストレスを軽減するためのシンプルな方法が学べる本です。"},
        {"book_title": "人を動かす", "review": "人間関係をより良くするためのコミュニケーション術が学べます。"},
        {"book_title": "内向型のあなたが才能を活かす方法", "review": "内向的な自分を肯定し、強みを活かす方法を示してくれます。"},
        {"book_title": "世界一やさしい「やる気」の言葉", "review": "モチベーションを高めるための優しい言葉が集められています。"},
        {"book_title": "引き寄せの法則", "review": "自分の思考が現実を作り出すという理論に基づいた本です。"},
        {"book_title": "スティーブ・ジョブズ 驚異のプレゼン", "review": "熱い情熱と集中力で成果を出す方法を学べる本です。"},
        {"book_title": "GRIT: やり抜く力", "review": "情熱と粘り強さが成功の鍵であることを教えてくれる本です。"},
        {"book_title": "モチベーション3.0", "review": "内発的動機づけを高めるための方法が学べます。"}
    ]
    
    book_recommendations = []
    for review in reviews:
        # 各レビューに対して感情分析を実行
        sentiment, _ = analyze_sentiment(review["review"])
        
        # 感情分析に基づいて本を推薦
        if sentiment == diary_sentiment:  # 日記の感情に一致する本のみ追加
            book_recommendations.append({
                "book_title": review["book_title"],
                "review": review["review"],
                "sentiment": sentiment
            })
    
    return book_recommendations
