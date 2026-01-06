# 使用官方 Python 3.11 slim 映像 (更小且穩定)
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製依賴文件
COPY requirements.txt .

# 安裝依賴 (使用 --no-cache-dir 減少映像大小)
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . .

# 設定預設端口 (Zeabur 會覆蓋此值)
ENV PORT=8080

# 暴露端口
EXPOSE 8080

# 啟動命令 (Shell 模式, 自動展開變數)
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app

