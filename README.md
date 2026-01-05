# 易經占卜陳老師 - 純 HTML/CSS/JS 版本

## 🎨 特色

- ✅ **完美的東方術數風格**：深墨色漸層背景、朱砂紅、古金色
- ✅ **前後端分離**：Flask API + 純前端
- ✅ **保留所有功能**：占卜、卦象查詢、AI 解讀
- ✅ **更大的輸入框**：3行高度，方便輸入
- ✅ **流暢動畫**：水墨暈染效果

## 📁 文件結構

```
卜卦主程式_新版/
├── frontend/
│   ├── index.html      # 主頁面
│   ├── style.css       # 東方術數風格
│   └── script.js       # 前端邏輯
├── backend/
│   └── api.py          # Flask API
├── requirements.txt    # Python 依賴
└── README.md          # 本文件
```

## 🚀 啟動方式

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 設定 OpenAI API Key（可選）

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key-here"

# Linux/Mac
export OPENAI_API_KEY="your-api-key-here"
```

### 3. 啟動後端

```bash
python backend/api.py
```

後端會在 `http://localhost:5000` 運行

### 4. 開啟前端

直接用瀏覽器開啟 `frontend/index.html`

或使用 Live Server（VS Code 擴展）

## 🎯 使用方式

1. 在輸入框中輸入問題
2. 點擊「🔮 送出」或按 Enter
3. 查看 AI 回應

### 範例問題

- 「我現在換工作，發展會如何？」（占卜）
- 「陳老師的聯絡方式」（背景問題）
- 「第1卦是什麼？」（卦象查詢）

## 🎨 設計細節

### 配色方案
- **背景**：深墨色漸層 `#0a0a0a → #1a1410 → #2d2416`
- **主色**：朱砂紅 `#c8102e`
- **輔色**：古金色 `#d4af37`
- **文字**：米白色 `#f5f5dc`

### 視覺元素
- 水墨暈染背景
- 竹簡風格卡片
- 朱砂印章風格按鈕
- 古卷風格訊息框
- 古銅色滾動條

## ⚠️ 注意事項

- 確保後端 API 正在運行
- 如未設定 OPENAI_API_KEY，AI 解讀功能將受限
- 建議使用現代瀏覽器（Chrome, Firefox, Edge）

## 📞 聯絡資訊

- Email: 13773023@scu.edu.tw
- 工作室：桃園市
