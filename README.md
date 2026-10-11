# Stegano App - Docker + CI/CD + Мониторинг

Веб-приложение для стеганографии: прячет EXE-файлы внутри PNG-изображений. Полностью контейнеризировано, автоматически собирается через GitHub Actions, разворачивается через Docker Compose, имеет мониторинг через Prometheus и Grafana. Само приложение было разработано в рамках учебной дисциплины "Защита информации" на втором курсе.

<img width="1327" height="590" alt="image" src="https://github.com/user-attachments/assets/bfe986dc-612e-462c-a8b1-346d931bc778" />


## Что умеет приложение

- **Скрыть EXE в PNG** - кодирует исполняемый файл в младшие биты пикселей изображения.
- **Извлечь EXE из PNG** - восстанавливает исходный файл из картинки.

## Технологии

| Компонент | Назначение |
|---|---|
| Python 3.10 + Flask | Backend приложения |
| Pillow | Работа с изображениями |
| Docker | Контейнеризация |
| Docker Compose | Оркестрация стека |
| GitHub Actions | CI/CD (сборка + push образа) |
| Prometheus | Сбор метрик |
| Grafana | Визуализация метрик |



## Быстрый старт

### Запуск

```bash
git clone https://github.com/Derro709/DockerPractice.git
cd DockerPractice
docker-compose up -d --build
```

После запуска доступны:

| Сервис | URL | Логин/пароль |
|---|---|---|
| Приложение | http://localhost:5000 | - |
| Health check | http://localhost:5000/health | - |
| Метрики | http://localhost:5000/metrics | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin / admin |

### Остановка

```bash
docker-compose down
```

Данные Grafana сохраняются в volume `grafana_data`.

## Метрики

Приложение отдаёт:

- Общее число запросов (счётчик посещений).
- Health check (1 = живо, 0 = упало).
- Потребление CPU.
- Потребление RAM.
<img width="1356" height="616" alt="image" src="https://github.com/user-attachments/assets/37de0eea-e054-45e3-9b69-93dc97874f76" />

