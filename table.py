from terminaltables import AsciiTable

def generate_table_of_vacancies(languages, site):
    data_for_table = [['Язык программирования', 'Вакансий найдено',
            'Ваканский обработано', 'Средняя зарплата']]
    for lang_name, lang_statistic in languages.items():
        data_for_table.append([lang_name,
                    lang_statistic['vacancies_found'],
                    lang_statistic['vacancies_processed'],
                    lang_statistic['average_salary']])
    table = AsciiTable(data_for_table)
    table.title = f'{site} Moscow'
    return table

