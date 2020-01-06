import requests
import os
from dotenv import load_dotenv
from itertools import count
from statistics import mean
from table import get_table

load_dotenv()

def get_vacancies():
    SECRET_KEY_SUPER_JOB = os.getenv('SECRET_KEY_SUPER_JOB')
    headers = {
        'X-Api-App-Id': SECRET_KEY_SUPER_JOB
    }
    url = 'https://api.superjob.ru/2.0/vacancies'
    for page in count():
        page_response= requests.get(url, headers=headers, params={
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
        if vacancie['currency'] == 'rub':
            if language in vacancie['profession'].lower():
                count_language += 1
                if vacancie['payment_from'] and vacancie['payment_to']:
                    salary = int((vacancie['payment_from'] + vacancie['payment_to']) / 2)
                    salaries.append(salary)
                elif vacancie['payment_from']:
                    salary = int(vacancie['payment_from'] * 1.2)
                    salaries.append(salary)
                elif vacancie['payment_to']:
                    salary = int(vacancie['payment_to']*0.8)
                    salaries.append(salary)
    if salaries:
        avg_salary = int(mean(salaries))
    else: avg_salary = 0
    vacancies_processed = len(salaries)
    data = {
        'vacancies_found': count_language,
        'vacancies_processed': vacancies_processed,
        'average_salary': avg_salary
    }
    return data

def get_languages():
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
