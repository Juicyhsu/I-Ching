# Zeabur 部署參考手冊

這份文件匯總了本專案在 Zeabur 部署成功的所有關鍵配置與注意事項。未來重新部署或遷移時可參照此文件。

## 1. 專案結構關鍵點

```
.
├── backend/
│   ├── api.py           # 主程式 (Flask app)
│   └── __init__.py      # ⚠️ 必須存在，否則找不到模組
├── frontend/
│   ├── index.html       # 主頁
│   ├── script.js        # 前端邏輯 (含 API URL 配置)
│   └── *.mp4            # ⚠️ 影片必須放在這裡，Flask 才能 serve
├── Dockerfile           # 構建配置
├── zbpack.json          # Zeabur 專屬配置 (健康檢查)
└── requirements.txt     # Python 依賴
```

## 2. 關鍵配置文件

### Dockerfile
使用 `python:3.11-slim` 以減少映像檔大小 (~60MB)。

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# 支援中文與實時日誌
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Zeabur 動態分配端口
ENV PORT=8080
EXPOSE 8080

# ⚠️ 必須使用 Shell 模式以支援變數擴展
CMD gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 1 --threads 8 --timeout 120 --access-logfile - --error-logfile - --log-level info app:app
```

### zbpack.json
配置健康檢查，確保部署零停機。

```json
{
  "start_command": "sh -c 'gunicorn --bind 0.0.0.0:${PORT:-8080} ...'",
  "healthcheck": {
    "path": "/health",
    "interval": 10,
    "timeout": 5,
    "retries": 3
  }
}
```

### requirements.txt
OpenAI SDK 必須使用新版以支援 `proxies` 參數。
- `openai>=1.58.1`

### .dockerignore
**不要**排除 `.mp4` 文件，否則影片無法顯示。
```gitignore
# 保留必要的
.git
__pycache__
*.md
# ⚠️ 注意：不要添加 *.mp4
```

## 3. 前端配置 (script.js)
前端必須能自動判斷環境 (本地 vs Zeabur)。

```javascript
// 自動判斷 API URL
const isFileProtocol = window.location.protocol === 'file:';
const isLocalhost = window.location.hostname === 'localhost';

if (isFileProtocol || isLocalhost) {
    API_URL = 'http://localhost:8080'; // 或 5001
} else {
    API_URL = ''; // 生產環境使用相對路徑 (同源)
}
```

## 4. Zeabur 環境變數設定
在 Zeabur 控制台 -> Variables 中設定：

| 變數名 | 值 | 說明 |
|--------|----|------|
| `OPENAI_API_KEY` | `sk-proj-...` | 必填，否則 AI 功能無效 |
| `PORT` | `8080` | (Zeabur 通常會自動注入，但可手動設定保險) |

## 5. 常見問題 (FAQ)

### Q: 部署後出現 502 Bad Gateway？
- **原因 1**: Dockerfile 啟動命令使用了硬編碼端口 (如 5001)，而 Zeabur 分配了其他端口。
  - **解法**: 確保使用 `${PORT:-8080}`。
- **原因 2**: 缺少 `backend/__init__.py` 導致 Python 找不到模組。
- **原因 3**: `app:app` 指向錯誤。確保 `app.py` 中有 `app = Flask(...)` 對象。

### Q: 影片無法播放 (404)？
- **原因 1**: 影片放在根目錄，但 Flask 只設定了 `frontend` 為靜態資料夾。
  - **解法**: 移動影片到 `frontend/` 資料夾。
- **原因 2**: `.dockerignore` 排除了 `.mp4`。
  - **解法**: 檢查並移除排除規則。

### Q: 部署失敗 (Evicted / OOM)？
- **原因**: 映像檔太大 (包含不必要的大檔)。
- **解法**: 使用 `.dockerignore` 排除不必要的測試影片或素材，並使用 `python:slim` 映像。
