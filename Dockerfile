FROM python:3.11-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . .
RUN pip install pipenv; \
    pip install "psycopg[binary]"; \
    pipenv requirements > requirements.txt; \
    pip install -r requirements.txt \
    
