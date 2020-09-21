'''pageObject module'''

from locators import MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support import expected_conditions as EC

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

class SQLResultTable(object):
    """SQL Result table as PageObject"""

    def __init__(self, driver):
        #@param driver - selenium web driver
        '''standart init'''
        self.table = driver.find_element(*MainPageLocators.RESULT_TABLE)
        self.rows = self.table.find_elements(*MainPageLocators.RESULT_ROWS)
        self.column_names_dict = self.__get_column_names_iters_dict__()

    def __get_column_names_iters_dict__(self):
        '''returns dict of "column_name":iter dict'''
        column_names_dict = {}
        for i,col in enumerate(self.rows[0].find_elements(*MainPageLocators.RESULT_COLNAMES)):
            column_names_dict.update({col.text:i})
        return column_names_dict

    def __get_iter_from_column_name__(self, column_name):
        #@param column_name - name of the column in sql
        '''returns iter from "column_name":iter dict'''
        try:
            self.column_names_dict[column_name]
        except:
            raise ValueError("no column name '{}' in the table".format(column_name))
        return self.column_names_dict[column_name]

    def get_row_by_id(self, id):
        #@param id - id of the column to return, integer
        '''returns row as object by id'''
        return self.rows[id]

    def get_row_with_column_name(self, column_name, value):
        #@param column_name - column name, string
        #@param value - value of the column, string or integer
        '''returns value of the column or raises ValueError, if there are no such row'''
        iter = self.__get_iter_from_column_name__(column_name)
        for row in self.rows:
            print(row.text)
            cols = row.find_elements(*MainPageLocators.RESULT_COLS)
            if cols:
                if cols[iter].text == str(value):
                    return row
        raise ValueError("there are no rows with '{}' = '{}' were found".format(column_name, value))

    def get_column_value(self, row, column_name):
        #@param row - row to search in, selemium object
        #@param column_name - name of column to get value from, string
        '''returns column value from the row'''
        iter = self.__get_iter_from_column_name__(column_name)
        cols = row.find_elements(*MainPageLocators.RESULT_COLS)
        return cols[iter].text
    
    def get_rows_number(self):
        '''returns rows number of the table'''
        result = 0
        for row in self.rows:
            cols = row.find_elements(*MainPageLocators.RESULT_COLS)
            if cols: result += 1
        return result

    def if_values_in_row(self, values, row):
        #@param values - values to check, list
        #@param row - row to search in, selemium object
        """checks if values in row"""
        for val in values:
            if str(val) not in row.text:
                return False
        return True


class SQLPage(BasePage):
    '''SQLPage as PageObject'''

    def wait_until_element_is_presented(self, element):
        #@param element - Selenium element, Selenium object
        '''method to wait element to be presented on the page'''
        try:
            el = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(element)
            )
        finally:
            ElementNotVisibleException()

    def set_input_value(self, newValue):
        #@param newValue - new value to input in area, string
        '''method to input text into input area'''
        # changes value in SQL input
        script = 'window.editor.doc.setValue("{}")'.format(newValue)
        self.driver.execute_script(script)

    def click_runsql_button(self):
        """clicks RUN SQL button"""
        element = self.driver.find_element(*MainPageLocators.RUNSQL_BUTTON)
        element.click()

    def get_input_value(self):
        """returns input value"""
        script = 'return window.editor.doc.getValue()'
        return self.driver.execute_script(script)
