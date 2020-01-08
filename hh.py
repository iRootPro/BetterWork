import requests
from itertools import count
from statistics import mean
from salary import predict_rub_salary


def get_vacancies():
    url = 'https://api.hh.ru/vacancies'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/79.0.3945.79 Safari/537.36'}
    for page in count(0):
        page_response = requests.get(url, params={
            'specialization': '1.221',
            'area': 1,
            'period': 30,
            'per_page': 100,
            'page': page
        }, headers=headers)
        page_response.raise_for_status()
        page_data = page_response.json()
        if page >= page_data['pages'] - 1:
            break
        yield from page_data['items']


def predict_rub_salary_for_HeadHunter(language):
    vacancies = get_vacancies()
    salaries = []
    count_language = 0
    for vacancie in vacancies:
        if not vacancie['salary']:
            continue
        if not vacancie['salary']['currency'] == 'RUR':
            continue
        if language in vacancie['name'].lower():
            count_language += 1
            salary = predict_rub_salary(
                vacancie['salary']['from'], vacancie['salary']['to']
                )

            salaries.append(salary)
    if salaries:
        avg_salary = int(mean(salaries))
    else:
        avg_salary = 0
    vacancies_processed = len(salaries)

    data = {
        'vacancies_found': count_language,
        'vacancies_processed': vacancies_processed,
        'average_salary': avg_salary
    }
    return data


def get_languages_statistic():
    languages = {
        'Python': predict_rub_salary_for_HeadHunter('python'),
        'Java': predict_rub_salary_for_HeadHunter('java'),
        'JavaScript': predict_rub_salary_for_HeadHunter('javascript'),
        'PHP': predict_rub_salary_for_HeadHunter('php'),
        'Ruby': predict_rub_salary_for_HeadHunter('ruby'),
        'C++': predict_rub_salary_for_HeadHunter('c++'),
        'Swift': predict_rub_salary_for_HeadHunter('Swift'),
        'Go': predict_rub_salary_for_HeadHunter('go')
    }
    return languages
