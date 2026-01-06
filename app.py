#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zeabur 入口文件 - 支援 Gunicorn 和直接執行
"""
import os
import sys

# 確保可以 import backend 模組
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.api import app

# Gunicorn 會直接使用這個 app 物件
# 不需要在 if __name__ == '__main__' 裡面

if __name__ == '__main__':
    # 只有直接執行 python app.py 時才會進入這裡
    port = int(os.getenv('PORT', 5001))
    print(f"🚀 Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
