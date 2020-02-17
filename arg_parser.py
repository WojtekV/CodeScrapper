import argparse


class ConsoleArgParser:
    """A class used to parse arguments from command line

    Console arguments:
        email (str): user email - required
        password (str): user password - required
        driverpath (str): path to webdriver- required
        waittime (int): wait time for a website - optional
        outputname (str): name of folder which will store problems - optional

    """

    @staticmethod
    def get_arguments():
        """Creates, adds and parses arguments from command line

        Returns:
            class containing command line arguments

        """
        parser = argparse.ArgumentParser(description='CodeScrapper')
        parser.add_argument('-e', '--email', required=True, help='User email')
        parser.add_argument('-p', '--password', required=True, help='User password')
        parser.add_argument('-dr', '--driverpath', required=True, help='Absolute path to webdriver')
        parser.add_argument('-t', '--waittime', type=int, default=5, help='Wait time for a website to load. When '
                                                                          'error occurs, try add higher wait time ('
                                                                          'default=5)')
        parser.add_argument('-o', '--outputname', default='Problems', help='Name of output folder (default=Problems)')
        return parser.parse_args()