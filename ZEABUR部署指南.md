# Zeabur 部署指南

## 問題診斷

### 原始錯誤
```
TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
```

### 根本原因
1. **OpenAI SDK 版本過舊**: `openai==1.12.0` 與 Python 3.13 不兼容
2. **映像檔過大**: 443MB 導致節點儲存空間不足
3. **缺少優化配置**: 沒有 `.dockerignore` 和 `Dockerfile`

## 解決方案

### 1. 更新依賴套件 ✅
已將 `requirements.txt` 更新為:
```txt
flask==3.1.0
flask-cors==5.0.0
openai==1.58.1        # 從 1.12.0 更新到最新版
python-dotenv==1.0.1
gunicorn==23.0.0
```

### 2. 創建 .dockerignore ✅
排除不必要的文件:
- Markdown 文件 (*.md)
- 大型媒體文件 (*.mp4, *.png)
- Git 和 IDE 配置

### 3. 創建優化的 Dockerfile ✅
- 使用 `python:3.11-slim` (更小且穩定)
- 使用 `--no-cache-dir` 減少映像大小
- 配置 Gunicorn 參數

## 部署步驟

### 方法 1: 通過 GitHub (推薦)

1. **提交更改到 GitHub**
   ```bash
   git add .
   git commit -m "fix: 更新 OpenAI SDK 並優化 Docker 配置"
   git push origin main
   ```

2. **在 Zeabur 重新部署**
   - 進入 Zeabur 控制台
   - 選擇您的服務
   - 點擊 "Redeploy" 或等待自動部署

### 方法 2: 本地測試

1. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

2. **本地運行**
   ```bash
   python app.py
   ```

3. **Docker 測試** (可選)
   ```bash
   docker build -t i-ching-app .
   docker run -p 5001:5001 --env-file .env i-ching-app
   ```

## 環境變數設定

確保在 Zeabur 中設定以下環境變數:

```
OPENAI_API_KEY=sk-proj-xxxxx
PORT=5001
```

## 預期結果

- ✅ 映像檔大小減少 (預計 < 200MB)
- ✅ 部署成功,無 TypeError
- ✅ 應用程式正常運行

## 故障排除

### 如果仍然失敗:

1. **檢查環境變數**: 確保 `OPENAI_API_KEY` 已設定
2. **查看日誌**: 在 Zeabur 控制台查看完整錯誤訊息
3. **清除緩存**: 在 Zeabur 中刪除服務並重新創建
4. **聯繫支援**: 如果問題持續,聯繫 Zeabur 技術支援

## 參考資料

- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Zeabur 文檔](https://zeabur.com/docs)
- [Docker 最佳實踐](https://docs.docker.com/develop/dev-best-practices/)
