# Autotests task for Wisebits

for https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all

## Usage instructions:

 - Python 3.7
 - better to create virtual enviroment with packages, listed in *requirements.txt*
 - *get Chromium for your OS here: https://sites.google.com/a/chromium.org/chromedriver/downloads, put it into main directory*
 - all dependencies in requirements.txt
 - run in terminal `py.test -s tests.py --html=report.html`


 ## AUTHOR: Konstantin Chistyakov

 ## Задание:
 Используя любой язык программирования необходимо написать следующие автотесты для сайта https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all
1. Вывести все строки таблицы *Customers* и убедиться, что запись с ContactName равной ‘СGiovanni Rovelli’ имеет Address = ‘Via Ludovico il Moro 22’.
2. Вывести только те строки таблицы *Customers*, где city=‘London’. Проверить, что в таблице ровно 6 записей.
3. Добавить новую запись в таблицу *Customers* и проверить, что эта запись добавилась.
4. Обновить все поля (кроме CustomerID) в любой записи таблицы *Customers*и проверить, что изменения записались в базу.
5. Придумать собственный автотест и реализовать (тут все ограничивается только вашей фантазией). *Добавить новую запись в Customers, выбрать случайного клиента и заменить CustomerID во всех его заказах (Orders) на только что созданную запись, проверить, что изменения записались в базу*


Заполнить поле ввода можно с помощью js кода, используя объект window.editor.
Требования:
- Для реализации обязательно использовать Selenium WebDriver
- Код автотестов нужно выложить в любой git-репозиторий
