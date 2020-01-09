import sj
import hh
from dotenv import load_dotenv
from terminaltables import AsciiTable
import os

from table import generate_table_of_vacancies


def main():
    secret_key_super_job = os.getenv('SECRET_KEY_SUPER_JOB')
    superjob = generate_table_of_vacancies(
        sj.get_languages_statistic(secret_key_super_job), 'SuperJob')
    headhunter = generate_table_of_vacancies(
        hh.get_languages_statistic(), 'HeadHunter')
    print(superjob.table)
    print(headhunter.table)


if __name__ == '__main__':
    load_dotenv()
    main()

