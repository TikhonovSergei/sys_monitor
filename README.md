# System Monitor

Этот проект представляет собой системный монитор, который отображает текущую загрузку процессора, оперативной памяти и диска, а также позволяет записывать эти данные в базу данных и просматривать их.

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone <URL вашего репозитория>
    cd <название директории>
    ```

2. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

## Использование

Запустите приложение:
```sh
python main.py
```

## Основные функции

Начать запись: Начинает запись данных о системе в базу данных.
![alt text](https://github.com/user-attachments/assets/1731de16-f828-45f5-8a73-1c1e57210039)

Остановить запись: Останавливает запись данных.
![alt text](https://github.com/user-attachments/assets/e816dfd5-36ec-465d-8231-7eb235f15bae)

Интервалы обновления
Вы можете выбрать интервал обновления данных, нажав на одну из кнопок с интервалами.
![alt text](https://github.com/user-attachments/assets/4a25bcf6-5b8a-4b01-b439-f9b562d5884d)

Просмотр записей: Открывает окно с таблицей, содержащей все записи из базы данных.
![alt text](https://github.com/user-attachments/assets/6a8b2a39-4282-47f3-945d-4a5d768e96b8)

## Тестирование
Для запуска тестов используйте команду:
```sh
python -m unittest discover -s /Users/janinatikhonova/test_sys_monitor/tests -p 'test_*.py'
```
![alt text](https://github.com/user-attachments/assets/4b658674-fe89-49c4-9114-b046094c9012)

## Лицензия

Этот проект лицензирован под лицензией MIT. 

