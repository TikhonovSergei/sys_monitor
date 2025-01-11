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
`![alt text]([path/to/image](https://github.com/user-attachments/assets/1731de16-f828-45f5-8a73-1c1e57210039))`
![image]<img width="431" alt="image" src="https://github.com/user-attachments/assets/1731de16-f828-45f5-8a73-1c1e57210039" />

Остановить запись: Останавливает запись данных.
![image]<img width="427" alt="image" src="https://github.com/user-attachments/assets/e816dfd5-36ec-465d-8231-7eb235f15bae" />

Просмотр записей: Открывает окно с таблицей, содержащей все записи из базы данных.
![image]<img width="923" alt="image" src="https://github.com/user-attachments/assets/d40ed8d6-85c2-41b9-a840-795694f08046" />

Интервалы обновления
Вы можете выбрать интервал обновления данных, нажав на одну из кнопок с интервалами (1 сек, 2 сек, и т.д.).
![image]<img width="421" alt="image" src="https://github.com/user-attachments/assets/4a25bcf6-5b8a-4b01-b439-f9b562d5884d" />


## Тестирование
Для запуска тестов используйте команду:
```sh
python -m unittest discover -s /Users/janinatikhonova/test_sys_monitor/tests -p 'test_*.py'
```
![image]<img width="1001" alt="image" src="https://github.com/user-attachments/assets/4b658674-fe89-49c4-9114-b046094c9012" />

