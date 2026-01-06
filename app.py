#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zeabur 入口文件
"""
import os
from backend.api import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
