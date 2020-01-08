import requests
import os
from dotenv import load_dotenv
from itertools import count
from statistics import mean
from salary import predict_rub_salary
load_dotenv()

SECRET_KEY_SUPER_JOB = os.getenv('SECRET_KEY_SUPER_JOB')


def get_vacancies():
    headers = {
        'X-Api-App-Id': SECRET_KEY_SUPER_JOB
    }
    url = 'https://api.superjob.ru/2.0/vacancies'
    for page in count():
        page_response = requests.get(url, headers=headers, params={
            'town': 4,
            'catalogues': 48,
            'count': 20,
            'period': 0,
            'page': page
        })
        page_response.raise_for_status()
        page_data = page_response.json()
        if not page_data['more']:
            break

        yield from page_data['objects']


def predict_rub_salary_for_SuperJob(language):
    vacancies = get_vacancies()
    salaries = []
    count_language = 0
    for vacancie in vacancies:
        if not vacancie['currency'] == 'rub':
            continue
        if language not in vacancie['profession'].lower():
            continue
        count_language += 1
        if not vacancie['payment_from'] and vacancie['payment_to']:
            continue
        salary = predict_rub_salary(
            vacancie['payment_from'], vacancie['payment_to']
            )
        salaries.append(salary)
    if not salaries:
        avg_salary = 0
    else:
        avg_salary = int(mean(salaries))
    vacancies_processed = len(salaries)
    data = {
        'vacancies_found': count_language,
        'vacancies_processed': vacancies_processed,
        'average_salary': avg_salary
    }
    return data


def get_languages_statistic():
    languages = {
        'Python': predict_rub_salary_for_SuperJob('python'),
        'Java': predict_rub_salary_for_SuperJob('java'),
        'JavaScript': predict_rub_salary_for_SuperJob('javascript'),
        'PHP': predict_rub_salary_for_SuperJob('php'),
        'Ruby': predict_rub_salary_for_SuperJob('ruby'),
        'C++': predict_rub_salary_for_SuperJob('c++'),
        'Swift': predict_rub_salary_for_SuperJob('Swift'),
        'Go': predict_rub_salary_for_SuperJob('go')
    }
    return languages

