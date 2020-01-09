import requests
from itertools import count
from statistics import mean
import os
from salary import predict_rub_salary


def get_vacancies(secret_key_super_job):
    headers = {
        'X-Api-App-Id': secret_key_super_job
    }
    url = 'https://api.superjob.ru/3.0/vacancies'
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


def predict_rub_salary_for_SuperJob(language, secret_key_super_job):
    vacancies = get_vacancies(secret_key_super_job)
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


def get_languages_statistic(secret_key_super_job):
    languages = {
        'Python': predict_rub_salary_for_SuperJob('python', secret_key_super_job),
        'Java': predict_rub_salary_for_SuperJob('java', secret_key_super_job),
        'JavaScript': predict_rub_salary_for_SuperJob('javascript', secret_key_super_job),
        'PHP': predict_rub_salary_for_SuperJob('php', secret_key_super_job),
        'Ruby': predict_rub_salary_for_SuperJob('ruby', secret_key_super_job),
        'C++': predict_rub_salary_for_SuperJob('c++', secret_key_super_job),
        'Swift': predict_rub_salary_for_SuperJob('Swift', secret_key_super_job),
        'Go': predict_rub_salary_for_SuperJob('go', secret_key_super_job)
    }
    return languages

