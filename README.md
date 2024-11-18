# REST API для расчета стоимости страхования

## Функционал
- Загрузка тарифов из JSON.
- Расчет стоимости страхования на основе актуального тарифа.
- Хранение данных в базе PostgreSQL.
- Простое развертывание с Docker Compose.

---

## Технологии
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker и Docker Compose

---

## Запуск
1. Клонируйте репозиторий:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   
2. Запустить PostgreSQL (если ещё не установлен):
   ```bash
   docker run --name smit -e POSTGRES_PASSWORD=Smit123. -d postgres:13

3. Подключиться к PostgreSQL через консоль:
   ```bash
   docker exec -it my_postgres psql -U postgres
   CREATE DATABASE db_smit;
   CREATE USER smit WITH PASSWORD 'Smit123.';
   GRANT ALL PRIVILEGES ON DATABASE db_smit TO smit;
