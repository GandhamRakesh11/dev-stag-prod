# -------- Base Image --------
FROM python:3.11-slim

# -------- Environment --------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -------- Working Directory --------
WORKDIR /app

# -------- Install Dependencies --------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -------- Copy Application Code --------
COPY app.py .

# -------- Expose Port --------
EXPOSE 5000

# -------- Start Application --------
CMD ["python", "app.py"]
