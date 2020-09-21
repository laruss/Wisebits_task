"""Autotests task for Wisebits, author: Chistyakov Konstantin"""
import pytest
import page, settings
from locators import MainPageLocators
import random, time

class TestUnit:
    def setup(self):
        """Basic setup method"""
        self.driver = settings.WEBDRIVER(executable_path=settings.EXEC_PATH)
        self.driver.get(settings.PAGE)
        self.START_SQLCODE = "SELECT * FROM Customers;"
        self.sql_page = page.SQLPage(self.driver)

    def teardown(self):
        """Basic teardown method"""
        self.driver.quit()

    def scenario_check_input_and_run_sql(self, sql_code):
        #@param sql_code - SQL code as string
        '''checks input field and runs sql'''
        #check value in input
        assert sql_code in self.sql_page.get_input_value()
        #click on Run SQL button
        self.sql_page.click_runsql_button()
        #awaits 1 sec till SQL executes
        time.sleep(1)

    def scenario_input_and_run_sql(self, sql_code):
        #@param sql_code - SQL code as string
        '''input in input field and runs sql'''
        #input value in input
        self.sql_page.set_input_value(sql_code)
        #runs sql
        self.scenario_check_input_and_run_sql(sql_code)

    def test_01_select_all(self):
        """
        1. Вывести все строки таблицы *Customers* и убедиться, что запись 
            с ContactName равной ‘СGiovanni Rovelli’ имеет Address = ‘Via Ludovico il Moro 22’.
        """
        #checks code in imput and run sql
        self.scenario_check_input_and_run_sql(self.START_SQLCODE)
        #waiting untill table will be visible
        self.sql_page.wait_until_element_is_presented(MainPageLocators.RESULT_TABLE)
        #set result table as SQLResultTable
        sql_results = page.SQLResultTable(self.driver)
        #get row with "CustomerName" = "СGiovanni Rovelli"
        row = sql_results.get_row_with_column_name("CustomerName", "СGiovanni Rovelli")
        #check if "Address" == "Via Ludovico il Moro 22"
        assert sql_results.get_column_value(row, "Address") == "Via Ludovico il Moro 22"
    
    def test_02_city_london(self):
        """
        2. Вывести только те строки таблицы *Customers*, где city=‘London’. 
            Проверить, что в таблице ровно 6 записей.
        """
        SELECT_SQL = "SELECT * FROM Customers WHERE city='London';"
        #set code and run
        self.scenario_input_and_run_sql(SELECT_SQL)
        #waiting untill table will be visible
        self.sql_page.wait_until_element_is_presented(MainPageLocators.RESULT_TABLE)
        #set result table as SQLResultTable
        sql_results = page.SQLResultTable(self.driver)
        #check if we have 6 rows
        assert sql_results.get_rows_number() == 6
    
    def test_03_add_new_row(self):
        """
        3. Добавить новую запись в таблицу *Customers* и проверить, что эта запись добавилась.
        """
        #SQL CODE
        CHECK_VALUES = ('Cardinal', 'Tom B. Erichsen', 'Skagen 21', 'Stavanger', '4006', 'Norway')
        SQL_INSERT = "INSERT INTO 'Customers' (CustomerName, ContactName, Address, City, PostalCode, Country)"
        SQL_INSERT += "VALUES {};".format(str(CHECK_VALUES))
        #checks code in imput and run sql
        self.scenario_check_input_and_run_sql(self.START_SQLCODE)
        #wait until table will be visible
        self.sql_page.wait_until_element_is_presented(MainPageLocators.RESULT_TABLE)
        #set result table as SQLResultTable
        sql_results = page.SQLResultTable(self.driver)
        #get initial rows number
        INITIAL_ROWS_NUM = sql_results.get_rows_number()
        #input and run insert code
        self.scenario_input_and_run_sql(SQL_INSERT)
        #input and run select code
        self.scenario_input_and_run_sql(self.START_SQLCODE)
        #waiting untill table will be visible
        self.sql_page.wait_until_element_is_presented(MainPageLocators.RESULT_TABLE)
        #set result table as SQLResultTable
        sql_results = page.SQLResultTable(self.driver)
        #get new rows number to compare with initial
        FINAL_ROWS_NUM = sql_results.get_rows_number()
        #check if we have +1 new row
        assert FINAL_ROWS_NUM == INITIAL_ROWS_NUM+1
        #get last row by id = FINAL_ROWS_NUM
        ADDED_ROW = sql_results.get_row_by_id(FINAL_ROWS_NUM)
        #check if last row has values that we added
        assert sql_results.if_values_in_row(CHECK_VALUES, ADDED_ROW) == True
    
    def test_04_change_all_values(self):
        """
        4. Обновить все поля (кроме CustomerID) в любой записи таблицы *Customers*и проверить,
            что изменения записались в базу.
        """
        DATA = {"CustomerName":"Konstantin", "ContactName":"Kos",
            "Address":"Pushkin str, 12B", "City":"Moscow", "PostalCode":"105523", "Country":"Russia"}
        #SQL code
        SQL_UPDATE = "UPDATE Customers SET " + "".join(["'{}'='{}', ".format(key,val) for key,val in DATA.items()])
        SQL_UPDATE = SQL_UPDATE[0:-2] + " WHERE CustomerID="
        #input and run select code
        self.scenario_check_input_and_run_sql(self.START_SQLCODE)
        #waiting untill table will be visible
        self.sql_page.wait_until_element_is_presented(MainPageLocators.RESULT_TABLE)
        #set result table as SQLResultTable
        sql_results = page.SQLResultTable(self.driver)
        #get initial rows number
        INITIAL_ROWS_NUM = sql_results.get_rows_number()
        #get row id to update
        ROW_NUM_TO_UPADATE = random.randint(1, INITIAL_ROWS_NUM)
        #SQL UPDATE code
        SQL_UPDATE = SQL_UPDATE + str(ROW_NUM_TO_UPADATE)
        #SQL SELECT code
        SQL_SELECT = self.START_SQLCODE[0:-1] + " WHERE CustomerID={}".format(ROW_NUM_TO_UPADATE)
        #input and run select code
        self.scenario_input_and_run_sql(SQL_UPDATE)
        #input and run select code
        self.scenario_input_and_run_sql(SQL_SELECT)
        #waiting untill table will be visible
        self.sql_page.wait_until_element_is_presented(MainPageLocators.RESULT_TABLE)
        #set result table as SQLResultTable
        sql_results = page.SQLResultTable(self.driver)
        #getting row
        row = sql_results.get_row_with_column_name("CustomerID", ROW_NUM_TO_UPADATE)
        #check if changes are valid
        assert sql_results.if_values_in_row([val for key,val in DATA.items()], row) == True

    def test_05_my_test_join(self):
        """
        5. Придумать собственный автотест и реализовать (тут все ограничивается только вашей фантазией)
        Добавить новую запись в Customers, выбрать случайного клиента и заменить CustomerID во всех его
        заказах (Orders) на только что созданную запись, проверить, что изменения записались в базу 
        """
        #SQL code
        CHECK_VALUES = ('Konstantin', 'Konstantin C.', 'Bauman, 12', 'Moscow', '123456', 'Russia')
        SQL_INSERT = "INSERT INTO 'Customers' (CustomerName, ContactName, Address, City, PostalCode, Country)"
        SQL_INSERT += "VALUES {};".format(str(CHECK_VALUES))
        SQL_ORDERS_SELECT = "SELECT * FROM Orders WHERE CustomerID ="
        SQL_ORDERS_UPDATE = "UPDATE Orders SET CustomerID="
        #checks code in imput and run sql
        self.scenario_check_input_and_run_sql(self.START_SQLCODE)
        #waiting untill table will be visible
        self.sql_page.wait_until_element_is_presented(MainPageLocators.RESULT_TABLE)
        #set result table as SQLResultTable
        sql_results = page.SQLResultTable(self.driver)
        #get initial rows number
        INITIAL_ROWS_NUM = sql_results.get_rows_number()
        #get row id to update
        ROW_ID_TO_UPDATE = random.randint(1, INITIAL_ROWS_NUM)
        #input and run insert code
        self.scenario_input_and_run_sql(SQL_INSERT)
        #id of new record will be INITIAL_ROWS_NUM+1, so
        #check that new record was added
        self.scenario_input_and_run_sql(self.START_SQLCODE)
        #waiting untill table will be visible
        self.sql_page.wait_until_element_is_presented(MainPageLocators.RESULT_TABLE)
        #set result table as SQLResultTable
        sql_results = page.SQLResultTable(self.driver)
        #get new rows number to compare with initial
        NEW_ROW_ID = sql_results.get_rows_number()
        #check if we have +1 new row
        assert NEW_ROW_ID == INITIAL_ROWS_NUM+1
        #getting row q-ty with CustomerID = ROW_NUM_TO_UPADATE
        self.scenario_input_and_run_sql(SQL_ORDERS_SELECT+str(ROW_ID_TO_UPDATE))
        #waiting untill table will be visible
        self.sql_page.wait_until_element_is_presented(MainPageLocators.RESULT_TABLE)
        #set result table as SQLResultTable
        sql_results = page.SQLResultTable(self.driver)
        #set q-ty of records affected
        affected_rows = sql_results.get_rows_number()
        #update all records in Orders with CustomerID = ROW_NUM_TO_UPADATE
        #input and run insert code
        self.scenario_input_and_run_sql(SQL_ORDERS_UPDATE+"{} WHERE CustomerID={}".format(NEW_ROW_ID, ROW_ID_TO_UPDATE))
        #input and run select code
        self.scenario_input_and_run_sql(SQL_ORDERS_SELECT+str(NEW_ROW_ID))
        #waiting untill table will be visible
        self.sql_page.wait_until_element_is_presented(MainPageLocators.RESULT_TABLE)
        #set result table as SQLResultTable
        sql_results = page.SQLResultTable(self.driver)
        #check if all records are changed
        assert affected_rows == sql_results.get_rows_number()



