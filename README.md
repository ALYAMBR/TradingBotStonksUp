### Сборка и запуск проекта

Сборка бэкенда moex:

В директории moex/ выполнить:

> mvn clean package

> docker build -t moex-backend:latest

Сборка бэкенда алгоритма:

В директории algo_api/ выполнить:

>docker build -t algo-back:latest

В директории с docker-compose.yml выполнить:

>docker-compose up


Бэкэнд алгоритма доступен на порту 8000, бэкенд moex доступен на порту 8080.