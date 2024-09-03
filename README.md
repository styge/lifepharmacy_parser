## Получение полной информации о товарах на сайте `https://www.lifepharmacy.com/` в категории `Shampoo`

## Задача
Используя фреймворк `Scrapy`, написать код программы для получения информации о товарах интернет-магазина из выбранной категории, информацию представлять в виде списка словарей (один товар - один словарь) и сохранить в файл с расширением `.json`

## Функционал
Создали код программы, используя фреймворк `Scrapy`. Скрипт позволяет:

- получить полную информацию о товарах с заранее заданной категории на сайте `https://www.lifepharmacy.com/`

- получить полную информацию о товарах с любой другой требующейся категории на сайте `https://www.lifepharmacy.com/`

- сохранить полученные данные в формате `.json`

## Установка

**Клонируем проект, командой в терминале:**

`git clone https://github.com/styge/lifepharmacy_parser.git && cd lifepharmacy_parser`

**Создаем виртуальную среду (для Python 3.x) командой:**

`python -m venv venv`

**Активируем виртуальную среду командой:**
- Windows:
`venv\Scripts\activate`

- MacOS/Linux:
`source venv/bin/activate`

**В директории проекта установим зависимости, используя `pip` и файл `requirements.txt` командой:**
`pip install -r requirements.txt`

## Запуск
**Находясь в директории проекта запустим скрипт командой:**

`scrapy crawl lifepharmacy -O test_product_data.json`

## Используемые инструменты

`Python` `Scrapy`
 
