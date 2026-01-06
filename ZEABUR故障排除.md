# Zeabur 部署故障排除指南

## 🔴 當前狀態
最新部署被 Zeabur 自動移除,仍然顯示 502 錯誤。

## 🔍 可能的原因

### 1. 健康檢查失敗
Zeabur 無法通過健康檢查端點驗證應用程式狀態。

**已實施的修復:**
- ✅ 添加 `/health` 根路徑健康檢查端點
- ✅ 創建 `zbpack.json` 明確指定健康檢查配置
- ✅ 添加詳細的日誌輸出 (`--log-level info`)

### 2. 環境變數問題
`OPENAI_API_KEY` 未在 Zeabur 中設定,可能導致應用程式啟動失敗。

**檢查步驟:**
1. 前往 Zeabur 控制台
2. 選擇您的服務
3. 進入 "Variables" 標籤
4. 確認 `OPENAI_API_KEY` 已設定

### 3. PORT 綁定問題
Dockerfile 的 CMD 語法可能無法正確處理環境變數。

**已實施的修復:**
- ✅ 使用啟動腳本 (`start.sh`) 處理環境變數
- ✅ 改用 exec 形式的 CMD 指令

### 4. 啟動超時
應用程式啟動時間過長,超過 Zeabur 的超時限制。

**已實施的優化:**
- ✅ 映像檔大小減少到 ~57MB
- ✅ 使用 Python 3.11-slim 基礎映像

## 📋 最新修復內容

### 1. 添加健康檢查端點
```python
@app.route('/health')
def health_root():
    """根路徑健康檢查 (Zeabur 使用)"""
    return jsonify({
        'status': 'ok', 
        'service': 'i-ching', 
        'openai': 'enabled' if client else 'disabled'
    })
```

### 2. 創建 zbpack.json
```json
{
  "healthcheck": {
    "path": "/health",
    "interval": 10,
    "timeout": 5,
    "retries": 3
  }
}
```

### 3. 優化 Dockerfile
```dockerfile
# 創建啟動腳本
RUN echo '#!/bin/sh\nexec gunicorn --bind 0.0.0.0:$PORT ...' > /app/start.sh && chmod +x /app/start.sh

# 使用 exec 形式啟動
CMD ["/bin/sh", "/app/start.sh"]
```

## 🚀 下一步操作

### 方案 A: 檢查 Zeabur 日誌 (推薦)
1. 前往 Zeabur 控制台
2. 查看 "Runtime Logs"
3. 尋找錯誤訊息:
   - `ModuleNotFoundError`
   - `Address already in use`
   - `Health check failed`
   - 環境變數相關錯誤

### 方案 B: 設定環境變數
確保在 Zeabur 中設定:
```
OPENAI_API_KEY=sk-proj-xxxxx
PORT=8080  (通常 Zeabur 會自動設定)
```

### 方案 C: 本地測試 Docker
```bash
# 構建映像
docker build -t i-ching-test .

# 運行容器
docker run -p 8080:8080 -e PORT=8080 -e OPENAI_API_KEY=your-key i-ching-test

# 測試健康檢查
curl http://localhost:8080/health
```

### 方案 D: 簡化部署 (如果以上都失敗)
移除 Dockerfile,讓 Zeabur 自動檢測 Python 應用程式:
1. 刪除 `Dockerfile`
2. 創建 `Procfile`:
   ```
   web: gunicorn --bind 0.0.0.0:$PORT app:app
   ```

## 📊 Git 提交歷史
```
d27ff83 - fix: 添加 /health 端點、zbpack.json 配置和優化 Dockerfile 啟動腳本
b773761 - docs: 更新部署指南說明 PORT 配置問題
f83c638 - fix: 修復 Dockerfile PORT 配置和前端 API URL 邏輯以解決 502 錯誤
0eca58f - fix: 更新 OpenAI SDK 到 1.58.1 並優化 Docker 配置以修復 Zeabur 部署錯誤
```

## ⚠️ 重要提醒
請在 Zeabur 重新部署後,**立即查看 Runtime Logs**,並將錯誤訊息提供給我,這樣我才能精確診斷問題。
