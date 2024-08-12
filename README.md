# Face Verification Service

Репозиторий с сервисом для проведения верификации лица пользователя.

От приложения ожидается использование [8080 порта](./.devcontainer/docker-compose.yml#L12) внутри контейнера.
На локальном хосте приложение будет доступно на [28080 порту](./.devcontainer/docker-compose.yml#L12).


## Описание сервиса

Сервис проведения транзакций представляет собой класс `FaceVerificationService`.

`FaceVerificationService` принимает в качестве аргумента объект `Repository`.

`Repository` - это интерфейс для доступа к хранилищу данных. Он служит для уменьшения связности и разворота зависимостей в сторону конкретных имплементаций модулей доступа к хранилищу данных.

`InMemoryRepository` - имплементация интерфейса Repository. Служит для сохранения данных в локальные структуры Python во время работы программы. Для хранения данных используются списки.


## Особенности

- Для верификации лица сервис использует библиотеку [DeepFace](https://pypi.org/project/deepface/).
- Для доступа к функциям сервиса используется API на базе HTTP запросов.
- Для хранения данных сервис использует базу данных [PostgreSQL](https://www.postgresql.org/).
- Для кэширования данных используется [Redis](https://redis.io/).
- Для получения информации о изображении переданном пользователем используется очередь сообщений [kafka](https://kafka.apache.org/).
- Настроенна сборка приложения в Docker контейнере.

## Используемые инструменты и технологии

- Python 3.12
- Fast API
- Pydantic
- DeepFace
- Linux
- Docker
- PostgreSQL
- Redis
- Kafka
- Kubernetes

## Локальная разработка и тестирование проекта

Проект разрабатывается в devcontainer. Информацию о том, как запустить проект и работать над ним, можно найти в файле [CONTRIBUTING.md](./CONTRIBUTING.md).

## Линтер

### Используемые утилиты

В проекте предусмотренно использование линтеров и статических анализаторов кода.

В проекте используются следующие линтеры и статические анализаторы кода:

- **wemake-python-styleguide** - линтер
- **MyPy** - статический анализатор кода

### Работа с линтером

Для запуска линтера установите все зависимости и создайте виртуальное окружение проекта, как это описано в файле [CONTRIBUTING.md](./CONTRIBUTING.md).

Затем выполните следующие команды в корне проекта:

Для запуска линтера **wemake-python-styleguide**:

```shell
poetry run flake8 --jobs=1 src
```

Для запуска статического анализатора кода **MyPy**:

```shell
poetry run mypy src/app
```
