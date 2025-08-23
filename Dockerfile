FROM python:3.11-slim

# Postavi radni direktorij
WORKDIR /app

# Kopiraj dependencies i instaliraj
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiraj aplikaciju
COPY . .

# Pokreni uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

