import sj
import hh
from table import generate_table_of_vacancies
from terminaltables import AsciiTable


def main():
    superjob = generate_table_of_vacancies(
        sj.get_languages_statistic(), 'SuperJob')
    headhunter = generate_table_of_vacancies(
        hh.get_languages_statistic(), 'HeadHunter')
    print(superjob.table)
    print(headhunter.table)


if __name__ == '__main__':
    main()

