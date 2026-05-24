# ۱. دریافت پایتون پایدار
FROM docker.arvancloud.ir/python:3.10-slim-bookworm

# ۲. تنظیمات محیطی
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# ۳. کپی فایل نیازمندی‌های تمیز شده
COPY requirements.txt /app/

# ۴. تنظیم پروکسی به صورت استاندارد + استثنا کردن سایت PyTorch برای جلوگیری از ارور SSL
ENV http_proxy="http://host.docker.internal:10808"
ENV https_proxy="http://host.docker.internal:10808"
ENV no_proxy="download.pytorch.org"

# ۵. نصب پکیج‌ها (الان سایت PyTorch رو بدون فیلترشکن و بدون ارور باز میکنه!)ص
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# ۶. کپی کدهای پروژه
COPY . /app/
EXPOSE 8000

# ۷. اجرا
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]