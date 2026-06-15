FROM python:3.13 AS backend

WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .

EXPOSE 5000
FROM node:20-alpine AS frontend

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ .
RUN npm run build


FROM python:3.13-slim

WORKDIR /app

COPY --from=backend /app/backend ./backend

COPY --from=frontend /app/frontend/dist ./frontend/dist

COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r ./backend/requirements.txt

EXPOSE 5000

WORKDIR /app/backend

CMD ["python", "app.py"] 