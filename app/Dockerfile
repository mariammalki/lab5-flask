# Image de base
FROM python:3.12-slim

# Dossier de travail
WORKDIR /app

# Copier le code source
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port Flask
EXPOSE 5000

# Démarrer l’application
CMD ["python", "app.py"]