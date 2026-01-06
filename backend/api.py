#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
易經占卜 API 服務器
提供占卜、卦象查詢、AI 解讀等功能
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import random
from datetime import datetime
from dotenv import load_dotenv

# ============================================================================
# 🔑 載入 .env 文件中的 API Key（安全方式）
# ============================================================================
# 從 .env 文件載入環境變數
load_dotenv()

# 如果您想直接在這裡填入（不推薦，僅供測試）
# OPENAI_API_KEY = "sk-proj-xxxxx"
# ============================================================================

# ============================================================================

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)  # 允許跨域請求

@app.route('/')
def index():
    return app.send_static_file('index.html')

# OpenAI 初始化
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None
    print("⚠️ 警告：未設定 OPENAI_API_KEY")

# 陳老師人設
CHEN_LAOSHI_PERSONA = """
你是資深占卜師「JeanTseng」的數位分身，被稱為「易經占卜陳老師」。

【基本資料】
- 姓名：JeanTseng
- 職業：資料分析師，對於易經占卜稍有研究
- 經驗：超過 20 年資料分析經驗
- 婚姻狀況：已婚，育有一子一女
- 居住地：桃園
- 星座：巨蟹座
- 年齡：不惑之年

【教育背景】
- 東吳大學資料科學研究所

【興趣】
- 旅遊
- 易經卜卦
- 閱讀
- 說笑話

【聯絡方式】
- Email:13773023@scu.edu.tw
- 工作室地址：桃園市

【服務理念】
陳老師認為，易經占卜不是宿命論，而是一種自我認識的工具。
透過易經卦象分析，幫助來訪者了解自己的優勢與挑戰，
從而做出更明智的人生選擇。

【回答風格】
請用溫和、專業、具同理心的語氣回答，像一位值得信賴的長輩或導師。
沒有找到答案，請回答"秘密"
"""

# 八卦數據
TRIGRAMS = {
    0: {'name': '坤', 'symbol': '☷', 'element': '地'},
    1: {'name': '乾', 'symbol': '☰', 'element': '天'},
    2: {'name': '兌', 'symbol': '☱', 'element': '澤'},
    3: {'name': '離', 'symbol': '☲', 'element': '火'},
    4: {'name': '震', 'symbol': '☳', 'element': '雷'},
    5: {'name': '巽', 'symbol': '☴', 'element': '風'},
    6: {'name': '坎', 'symbol': '☵', 'element': '水'},
    7: {'name': '艮', 'symbol': '☶', 'element': '山'},
    8: {'name': '坤', 'symbol': '☷', 'element': '地'}
}

# 64卦數據（簡化版 - 包含前10卦）
HEXAGRAMS = {
    '乾乾': {'num': 1, 'name': '乾為天', 'meaning': '元亨利貞。剛健中正，自強不息。', 'fortune': '大吉'},
    '坤坤': {'num': 2, 'name': '坤為地', 'meaning': '元亨，利牝馬之貞。', 'fortune': '吉'},
    '坎震': {'num': 3, 'name': '水雷屯', 'meaning': '元亨利貞，勿用有攸往。', 'fortune': '中平'},
    '艮坎': {'num': 4, 'name': '山水蒙', 'meaning': '亨。匪我求童蒙，童蒙求我。', 'fortune': '中下'},
    '坎乾': {'num': 5, 'name': '水天需', 'meaning': '有孚，光亨，貞吉。', 'fortune': '中上'},
    '乾坎': {'num': 6, 'name': '天水訟', 'meaning': '有孚，窒。惕中吉。', 'fortune': '下下'},
    '坤坎': {'num': 7, 'name': '地水師', 'meaning': '貞，丈人，吉無咎。', 'fortune': '中上'},
    '坎坤': {'num': 8, 'name': '水地比', 'meaning': '吉。原筮元永貞，無咎。', 'fortune': '上上'},
    '巽乾': {'num': 9, 'name': '風天小畜', 'meaning': '亨。密雲不雨。', 'fortune': '中下'},
    '乾兌': {'num': 10, 'name': '天澤履', 'meaning': '履虎尾，不咥人，亨。', 'fortune': '中上'},
}

def get_divination_numbers():
    """生成三個占卜數字"""
    return random.randint(100, 999), random.randint(100, 999), random.randint(100, 999)

def calculate_hexagram(num1, num2, num3):
    """計算卦象"""
    upper_trigram = TRIGRAMS.get(num2 % 8, TRIGRAMS[1])
    lower_trigram = TRIGRAMS.get(num1 % 8, TRIGRAMS[1])
    hexagram_key = f"{upper_trigram['name']}{lower_trigram['name']}"
    hexagram = HEXAGRAMS.get(hexagram_key, HEXAGRAMS['乾乾'])
    changing_line = 6 if (num3 % 6) == 0 else (num3 % 6)
    
    return {
        'upper_trigram': upper_trigram,
        'lower_trigram': lower_trigram,
        'hexagram': hexagram,
        'changing_line': changing_line,
        'numbers': (num1, num2, num3)
    }

def get_ai_interpretation(question, result):
    """獲取 AI 解讀"""
    if not client:
        return "（AI 解讀功能需要 OPENAI_API_KEY）\\n\\n根據卦象，這是一個關於變化與選擇的時刻。建議您保持內心平靜，審慎思考後再做決定。"
    
    hexagram = result['hexagram']
    upper = result['upper_trigram']
    lower = result['lower_trigram']
    changing_line = result['changing_line']
    
    prompt = f"""
你是易經占卜陳老師，請根據以下卦象為來訪者提供專業解讀。

【來訪者問題】
{question}

【卦象資訊】
本卦：第 {hexagram['num']} 卦 - {hexagram['name']}
上卦：{upper['name']}（{upper['element']}）{upper['symbol']}
下卦：{lower['name']}（{lower['element']}）{lower['symbol']}
卦義：{hexagram['meaning']}
運勢：{hexagram['fortune']}
變爻：第 {changing_line} 爻

請用溫和、專業的語氣提供解讀，包含實際建議（3-5點），字數控制在 300-400 字。
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是易經占卜陳老師。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"根據 {hexagram['name']} 的卦象，建議您保持{hexagram['fortune']}的心態。"

def determine_intent(question):
    """判斷用戶意圖"""
    question_lower = question.lower()
    
    divination_keywords = ["占卜", "算命", "運勢", "吉凶", "未來", "發展", "如何", "是否", "會不會"]
    persona_keywords = ["陳老師", "你", "您", "介紹", "背景", "聯絡"]
    
    divination_score = sum(1 for kw in divination_keywords if kw in question_lower)
    persona_score = sum(1 for kw in persona_keywords if kw in question_lower)
    
    if divination_score > persona_score:
        return 'DIVINATION'
    elif persona_score > 0:
        return 'PERSONA'
    else:
        return 'DIVINATION'

def get_ai_response(question, system_prompt):
    """獲取 AI 回應"""
    if not client:
        return "抱歉，AI 功能暫時無法使用。"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except:
        return "抱歉，我目前無法回答這個問題。"

@app.route('/api/chat', methods=['POST'])
def chat():
    """聊天 API"""
    data = request.json
    message = data.get('message', '')
    user_numbers = data.get('numbers', None)  # 接收使用者抽到的數字
    
    if not message:
        return jsonify({'error': '請輸入問題'}), 400
    
    intent = determine_intent(message)
    
    if intent == 'DIVINATION':
        # 占卜
        if user_numbers and len(user_numbers) == 3:
            # 使用使用者抽到的數字
            num1, num2, num3 = user_numbers
        else:
            # 自動生成（備用）
            num1, num2, num3 = get_divination_numbers()
        
        result = calculate_hexagram(num1, num2, num3)
        interpretation = get_ai_interpretation(message, result)
        
        hexagram = result['hexagram']
        upper = result['upper_trigram']
        lower = result['lower_trigram']
        
        response_text = f"""╔═════════════════════════════════╗
║  🔮  易經占卜陳老師為您解卦  🔮 ║
╚═════════════════════════════════╝

【您的問題】
{message}

【起卦數字】
{num1}, {num2}, {num3}

【卦象資訊】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
本卦：第 {hexagram['num']} 卦 - {hexagram['name']}
上卦：{upper['name']} {upper['symbol']} （象徵{upper['element']}）
下卦：{lower['name']} {lower['symbol']} （象徵{lower['element']}）

卦義：{hexagram['meaning']}
運勢：{hexagram['fortune']}
動爻：第 {result['changing_line']} 爻
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【陳老師解讀】
{interpretation}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 提醒：占卜是一種自我認識的工具，最終的決定權在您手中。
╚═════════════════════════════════════════════════════╝
"""
        
        return jsonify({
            'response': response_text,
            'intent': 'DIVINATION',
            'hexagram_data': hexagram
        })
    
    else:
        # 背景問題
        response_text = get_ai_response(message, CHEN_LAOSHI_PERSONA)
        return jsonify({
            'response': response_text,
            'intent': 'PERSONA'
        })

@app.route('/api/health', methods=['GET'])
def health():
    """健康檢查"""
    return jsonify({'status': 'ok', 'openai': 'enabled' if client else 'disabled'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    print("=" * 60)
    print("[*] 易經占卜 API 服務器啟動中...")
    print("=" * 60)
    if not OPENAI_API_KEY:
        print("[!] 警告：未設定 OPENAI_API_KEY")
    print(f"API 地址：http://0.0.0.0:{port}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=False)
