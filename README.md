# Catalog

Структура проекта:

- presentation: шлюз API приложения
- application: сложная единица бизнес-логики, делегирует задачи между более мелкими компонентами
- domain: единица бизнес логики, содержит модели и репозитории
- infrastructure: инкапсулирует код, который используется для создания всех вышеуказанных компонентов, реализует базовые классы
- config: настройки приложения

## Запуск приложения

Для первого развертывания необходимо запустить контейнер с БД.
```sh
docker compose up --build -d db
```
Создать базу данных, .env файл и настроить переменную DATABASE (host=localhost). Применить миграции и запустить скрипт для добавления тестовых данных
```sh
alembic upgrade head
poetry run add_test_data.py
```
Далее меняем host базы данных в .env на db, настраиваем по необходимости логирование (пример .env.example) и запускаем приложение
```sh
docker compose up --build -d app
```
Приложение запуститься на 8000 порте


## Реализация требований

Описание всех методов можно получить в /docs

Реализована регистрация и авторизация, чтобы выполнить требование по использованию API ключа. Поскольку в требованиях 
про это ничего не сказано, любой аутентифицированный пользователь будет иметь доступ ко всем данным. Добавлена привязка
пользователя к организации (наверное излишняя).

Все требования к апи реализованы в 2-ух эндпоинтах - получение организации по id, и поиск по фильтрам. Поскольку 
все фильтры реализованы в 1 эндпоинте, пользователь сможет искать организации по нескольким фильтрам.

Уровень вложенности был ограничен в рамках приложения с помощью event listener, однако поскольку добавление данных не 
реализовано, на данном этапе практического применения нет. Если необходимо обеспечить доп уровень безопасности 
можно создать триггер в БД, чтобы проверять уровни вложенности деятельностей. Это есть смысл делать, если данные в БД 
будут попадать извне нашего приложения.
