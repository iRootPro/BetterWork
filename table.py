from terminaltables import AsciiTable

def get_table(languages, site):
    data = [['Язык программирования', 'Вакансий найдено',
            'Ваканский обработано', 'Средняя зарплата']]
    for language in languages.items():
        data.append([language[0], language[1]['vacancies_found'],
                    language[1]['vacancies_processed'],
                    language[1]['average_salary']])
    table = AsciiTable(data)
    table.title = f'{site} Moscow'
    print(table.table)


