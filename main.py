from selenium import webdriver
from time import sleep
import os
import sys
from pathlib import Path
import argparse


class CodeScrapper:

    def __init__(self, email, password, driver_path, wait_time, output_name):
        self.email = email
        self.password = password
        self.driver_path = driver_path
        self.wait_time = wait_time
        self.problems_folder = output_name
        self.driver = webdriver.Chrome(executable_path=self.driver_path)

    def run(self):
        self.driver.get('https://leetcode.com/accounts/login')

        self.login()
        self.go_to_problems()
        self.create_problems_folder()

        problems = self.get_solved_problems_list()

        for p in problems:
            self.create_problem(p)

        print("Success! Solutions scrapped.")
        sys.exit()

    def login(self):
        self.driver.find_element_by_name('login').send_keys(self.email)
        self.driver.find_element_by_name('password').send_keys(self.password)
        sleep(self.wait_time)

        self.driver.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div[2]/div/div/div/button").click()
        sleep(self.wait_time)

    def go_to_problems(self):
        self.driver.find_element_by_xpath('//*[@id="lc_navbar"]/div/div[2]/ul[1]/li[3]/a').click()
        sleep(self.wait_time)

    def list_all_solved_questions_on_page(self):
        self.driver.find_element_by_xpath(
            '//*[@id="question-app"]/div/div[2]/div[2]/div[1]/div[2]/div[4]/button/div').click()
        self.driver.find_element_by_xpath(
            '//*[@id="question-app"]/div/div[2]/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="question-app"]/div/div[2]/div[2]/div[2]/table/tbody[2]/tr/td/span[1]/select/option[4]').click()

    def get_solved_problems_list(self):
        all_problems = self.driver.find_element_by_class_name('reactable-data')
        problems = []
        for p in all_problems.find_elements_by_tag_name('tr'):
            problem = str(p.find_element_by_tag_name('a').text).replace(' ', '_'), p.find_element_by_tag_name(
                'a').get_attribute('href')
            problems.append(problem)

        return problems

    def create_problem(self, p):
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
        ref_code = self.refactor_code(code.text)
        self.create_single_problem_solution(p, ref_code)
        sleep(self.wait_time / 2)
        self.driver.execute_script("window.history.go(-1)")

    def create_problems_folder(self):
        try:
            Path('output/' + self.problems_folder).mkdir(parents=True, exist_ok=False)
            self.problems_folder = 'output/' + self.problems_folder
        except OSError:
            sys.exit("Creation of folder '" + self.problems_folder + "' failed! Aborting..")

    def create_single_problem_solution(self, problem, code):
        if self.create_solution_folder(problem):
            if self.create_solution_file():
                self.write_code_to_file(code, problem)
            else:
                print('Creation of solution file ' + problem[0] + ' failed! Skipping the problem...')
        else:
            print('Creation of solution file ' + problem[0] + ' failed! Skipping the problem...')

    def create_solution_folder(self, problem):
        try:
            Path(self.problems_folder + '/' + problem[0]).mkdir(parents=True, exist_ok=False)
        except OSError:
            print('Creation of folder ' + problem[0] + ' failed! Skipping the problem...')
            return False
        return True

    @staticmethod
    def create_solution_file():
        try:
            open('solution.cpp', 'w+').close()
        except IOError:
            return False
        return True

    def write_code_to_file(self, code, problem):
        f = open('solution.cpp', 'w+')
        f.write(code)
        f.close()
        os.rename("solution.cpp", "./" + self.problems_folder + "/" + problem[0] + "/solution.cpp")

    def refactor_code(self, code):
        fun = ''
        blank_line = 0
        for l in code.splitlines():
            if not self.represents_int(l):
                if blank_line >= 2:
                    fun += '\n'
                fun += l + '\n'
                blank_line = 0
            else:
                blank_line += 1
        return fun

    @staticmethod
    def represents_int(i):
        try:
            int(i)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CodeScrapper')
    parser.add_argument('-e', '--email', required=True, help='User email')
    parser.add_argument('-p', '--password', required=True, help='User password')
    parser.add_argument('-dr', '--driverpath', required=True,  help='Absolute path to webdriver')
    parser.add_argument('-t', '--waittime', type=int, default=5, help='Wait time for a website to load. When error'
                                                                      ' occurs, try add higher wait time (default=5)')
    parser.add_argument('-o', '--outputname', default='Problems', help='Name of output folder (default=Problems)')
    args = parser.parse_args()
    CodeScrapper(args.email, args.password, args.driverpath, args.waittime, args.outputname).run()
