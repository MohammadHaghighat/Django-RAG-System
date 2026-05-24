# ۱. دریافت پایتون پایدار از میرور ایرانی (برای دور زدن تحریم‌ها)
FROM docker.devneeds.ir/python:3.10-slim-bookworm

# ۲. تنظیمات محیطی
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# ۳. کپی فایل نیازمندی‌های تمیز شده
COPY requirements.txt /app/

# ۴. نصب پکیج‌ها از میرور ایرانی + دریافت نسخه فوق سبک Torch (CPU-only) برای سرعت بالا
RUN pip install --no-cache-dir --default-timeout=200 -i https://pypi.devneeds.ir/simple/ -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# ۵. کپی کدهای پروژه
COPY . /app/
EXPOSE 8000

# ۶. اجرا
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]