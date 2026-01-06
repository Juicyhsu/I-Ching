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

# 暴露端口 (文檔用途)
EXPOSE 8080

# 創建啟動腳本
RUN echo '#!/bin/sh\nexec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - --log-level info app:app' > /app/start.sh && chmod +x /app/start.sh

# 啟動命令
CMD ["/bin/sh", "/app/start.sh"]

