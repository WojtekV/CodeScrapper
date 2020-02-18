from arg_parser import ConsoleArgParser
from selenium import webdriver
from pathlib import Path
from time import sleep
import sys
import os


class CodeScrapper:
    """A class used to scrap algorithm's solutions from www.leetcode.com website

    Class gets code from all solved c++ problems and creates folders and files for solutions code.

    Attributes:
        email (str): an user email used for login to website
        password (str): an password used for login to website
        driver_path (str): an absolute path to web driver. Must be chrome driver
        wait_time (int): an wait time for a web page load
        problems_folder (str): the name of folder where algorithms will be saved
        driver (WebDriver): the driver used for interaction with website

    """

    def __init__(self, email, password, driver_path, wait_time, output_name):
        """
        Arguments:
            email (str): user email
            password (str): user password
            driver_path (str): path to user's driver
            wait_time (int): wait time for a web page load
            output_name (str): name of folder where problems will be stored

        """
        self.email = email
        self.password = password
        self.driver_path = driver_path
        self.wait_time = wait_time
        self.problems_folder = output_name
        self.driver = webdriver.Chrome(executable_path=self.driver_path)

    def run(self):
        """Method runs all necessary functions in order to get problems solutions from website"""

        self.driver.get('https://leetcode.com/accounts/login')

        self._login()
        self._go_to_problems()
        self._create_output_folder()
        self._create_problems_folder()

        problems = self._get_solved_problems_list()

        for p in problems:
            self._create_problem(p)

        self.driver.close()
        print("Success! Solutions scrapped.")
        sys.exit()

    @staticmethod
    def _create_output_folder():
        """Creates output folder if not exists"""

        if not os.path.exists('output'):
            os.makedirs('output')

    def _login(self):
        """Login to www.leetcode.com website"""

        self.driver.find_element_by_name('login').send_keys(self.email)
        self.driver.find_element_by_name('password').send_keys(self.password)
        sleep(self.wait_time)

        self.driver.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div[2]/div/div/div/button").click()
        sleep(self.wait_time)

    def _go_to_problems(self):
        """Changes page to leetcode problems list"""

        self.driver.find_element_by_xpath('//*[@id="lc_navbar"]/div/div[2]/ul[1]/li[3]/a').click()
        sleep(self.wait_time)

    def _list_all_solved_questions_on_page(self):
        """Lists all solved questions"""

        self.driver.find_element_by_xpath(
            '//*[@id="question-app"]/div/div[2]/div[2]/div[1]/div[2]/div[4]/button/div').click()
        self.driver.find_element_by_xpath(
            '//*[@id="question-app"]/div/div[2]/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="question-app"]/div/div[2]/div[2]/div[2]/table/tbody[2]/tr/td/span[1]/select/option[4]').click()

    def _get_solved_problems_list(self):
        """Scraps problems from page and creates a list of strings from it

        Returns:
             problems (list): Solved problems list[str]
        """
        all_problems = self.driver.find_element_by_class_name('reactable-data')
        problems = []
        for p in all_problems.find_elements_by_tag_name('tr'):
            problem = str(p.find_element_by_tag_name('a').text).replace(' ', '_'), p.find_element_by_tag_name(
                'a').get_attribute('href')
            problems.append(problem)

        return problems

    def _create_problem(self, p):
        """Opens specific problem page, creates folder solution and copies code to file

        Arguments:
            p (list): first element of it is the name of problem, second is the link to problem

        """
        self.driver.get(p[1])
        sleep(self.wait_time/2)
        sleep(self.wait_time)
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[2]/div[1]/div/div[3]/div/div[1]/div/div[1]/div[2]/div[2]/button') \
            .click()
        sleep(self.wait_time)
        self.driver.find_element_by_xpath(
            '/html/body/div[7]/div/div[2]/div/div[2]/div[2]/div[2]/button[2]/div/span') \
            .click()
        sleep(self.wait_time)
        code = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[2]/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div[6]/div[1]/div/div/div/'
            'div[5]')
        ref_code = self._refactor_code(code.text)
        self._create_single_problem_solution(p, ref_code)
        sleep(self.wait_time / 2)
        self.driver.execute_script("window.history.go(-1)")

    def _create_problems_folder(self):
        """Creates folder for all problems"""

        try:
            Path('output/' + self.problems_folder).mkdir(parents=True, exist_ok=False)
            self.problems_folder = 'output/' + self.problems_folder
        except OSError:
            sys.exit("Creation of folder '" + self.problems_folder + "' failed! Aborting..")

    def _create_single_problem_solution(self, problem, code):
        """Creates solution for single problem"""

        if self._create_solution_folder(problem):
            if self._create_solution_file():
                self._write_code_to_file(code, problem)
            else:
                print('Creation of solution file ' + problem[0] + ' failed! Skipping the problem...')
        else:
            print('Creation of solution file ' + problem[0] + ' failed! Skipping the problem...')

    def _create_solution_folder(self, problem):
        """Creates single problem folder. Name of folder is the name of problem"""

        try:
            Path(self.problems_folder + '/' + problem[0]).mkdir(parents=True, exist_ok=False)
        except OSError:
            print('Creation of folder ' + problem[0] + ' failed! Skipping the problem...')
            return False
        return True

    @staticmethod
    def _create_solution_file():
        """Creates file for single solution"""

        try:
            open('solution.cpp', 'w+').close()
        except IOError:
            return False
        return True

    def _write_code_to_file(self, code, problem):
        """Writes code scrapped from website to file

        Arguments:
            code (str): refactored code scrapped from problem website
            problem (str): name of problem folder

        """
        f = open('solution.cpp', 'w+')
        f.write(code)
        f.close()
        os.rename("solution.cpp", "./" + self.problems_folder + "/" + problem[0] + "/solution.cpp")

    def _refactor_code(self, code):
        """Refactors code scrapped from website

        This operation is done because code is scrapped with line numbers.
        Function deletes lines containing numbers at the beginning of a line.

        Arguments:
             code (str): code scrapped from problem website

        """
        fun = ''
        blank_line = 0
        for l in code.splitlines():
            if not self._represents_int(l):
                if blank_line >= 2:
                    fun += '\n'
                fun += l + '\n'
                blank_line = 0
            else:
                blank_line += 1
        return fun

    @staticmethod
    def _represents_int(i):
        """Checks if variable is integer"""
        try:
            int(i)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    args = ConsoleArgParser.get_arguments()
    CodeScrapper(args.email, args.password, args.driverpath, args.waittime, args.outputname).run()
