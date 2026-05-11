## Тестовое задание: контейнеризация простого backend-приложения на Python и запуск его за Nginx reverse proxy.

Проект поднимает два сервиса:

- `back` — Python HTTP server;
- `nginx` — reverse proxy и единственная внешняя точка входа.

Используются:
- Python 3
- Nginx
- Docker
- Docker Compose

Backend не публикуется наружу напрямую и доступен только внутри Docker Compose network.


## Project structure

```text
.
├── back
│   ├── app.py
│   ├── Dockerfile
│   └── .dockerignore
├── nginx
│   └── default.conf
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Architecture

```text
Client
  |
  | http://localhost
  v
Nginx container
  |
  | proxy_pass http://back:8080
  v
Python backend container
```

Nginx принимает входящие HTTP-запросы на `80` порту и проксирует их во внутренний сервис `back` на порт `8080`.

Внешний доступ к backend-контейнеру не открыт. Это сделано намеренно: клиент взаимодействует только с reverse proxy, а backend остаётся внутренним сервисом.

## Implementation details

### Backend

Backend реализован как простой HTTP-сервер на Python.

Приложение слушает:

```text
0.0.0.0:8080
```

Использование `0.0.0.0` необходимо для корректной работы внутри контейнера: сервис должен принимать подключения не только с loopback-интерфейса контейнера, но и из Docker network.

Ожидаемый ответ на корневой маршрут:

```text
Hello from Effective Mobile!
```

### Dockerfile

Backend собирается из собственного `Dockerfile`.

Образ содержит только необходимые файлы приложения. Лишние локальные артефакты исключены через `.dockerignore`.

### Nginx

Nginx используется как reverse proxy.

Конфигурация находится в:

```text
nginx/default.conf
```

Основной upstream указывается через имя сервиса Docker Compose:

```nginx
proxy_pass http://back:8080;
```

`backend` — это DNS-имя сервиса внутри Docker Compose network. Использование `localhost` здесь было бы некорректным, потому что внутри контейнера Nginx `localhost` указывает на сам Nginx-контейнер.

### Docker Compose

`docker-compose.yml` описывает два сервиса:

- `backend` собирается из директории `./back`;
- `nginx` использует официальный образ `nginx:alpine`;
- наружу пробрасывается только порт Nginx;
- backend-порт доступен только внутри compose-сети.

## Run

Собрать и запустить проект:

```bash
docker compose up --build
```

После запуска приложение доступно по адресу:

```text
http://localhost
```

Проверка через `curl`:

```bash
curl http://localhost
```

Ожидаемый ответ:

```text
Hello from Effective Mobile!
```

## Run in background

```bash
docker compose up -d --build
```

Проверить статус контейнеров:

```bash
docker compose ps
```

Посмотреть логи:

```bash
docker compose logs
```

Логи конкретного сервиса:

```bash
docker compose logs nginx
```

```bash
docker compose logs backend
```

## Stop

Остановить и удалить контейнеры:

```bash
docker compose down
```

## Rebuild

После изменения кода backend или Dockerfile:

```bash
docker compose up --build
```

Либо для фонового режима:

```bash
docker compose down
docker compose up -d --build
```

## Ports

По умолчанию используется следующий mapping:

```text
host:80 -> nginx:80 -> backend:8080
```

Если порт `80` на хосте занят, можно изменить проброс в `docker-compose.yml`, например:

```yaml
ports:
  - "8080:80"
```

После этого приложение будет доступно по адресу:

```text
http://localhost:8080
```

## Repository contents

В репозиторий добавлены только исходники и конфигурация, необходимые для воспроизводимой сборки:

```text
back/app.py
back/Dockerfile
back/.dockerignore
nginx/default.conf
docker-compose.yml
.gitignore
README.md
```

Docker image не хранится в репозитории, так как он воспроизводимо собирается из `Dockerfile` командой:

```bash
docker compose up --build
```

## Quick check before review

```bash
docker compose down
docker compose up --build
```

В отдельном терминале:

```bash
curl http://localhost
```

Ожидаемый результат:

```text
Hello from Effective Mobile!
```
