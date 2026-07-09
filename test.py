# ============================================================
# test.py — To'g'ridan-to'g'ri ishga tushirish uchun
# ============================================================
# Ishlatish: python test.py
# ============================================================

import os
import sys

# Loyiha ildiz papkasini qo'shamiz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

# urls.py dan test funksiyasini import qilamiz
from account.urls import test, main

if __name__ == '__main__':
    print("\n🚀  test.py orqali ishga tushirilmoqda...\n")

    # Konsol uchun
    result = test()
    print("\n📋 main() JSON natijasi:\n")
    response = main()
    import json
    print(json.dumps(
        json.loads(response.content),
        indent=2,
        ensure_ascii=False
    ))