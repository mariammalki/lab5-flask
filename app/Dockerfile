# Utilise Python slim
FROM python:3.11-slim

WORKDIR /app

# Copier requirements
COPY requirements.txt .

# Installer pip à jour et les dépendances
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
