import requests
from itertools import count
from statistics import mean

def get_vacancies():
    url = 'https://api.hh.ru/vacancies'
    data = {
        'specialization': '1.221',
        'area': '1',
        'period': 30,
        'per_page': 100
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
    }
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

def get_programming_language():
    javascript = 0
    python = 0
    java = 0
    ruby = 0
    php = 0
    cpp = 0
    swift = 0
    go = 0
    all_vacancies = get_vacancies()
    for item in all_vacancies:
        if 'javascript' in item['name'].lower():
            javascript += 1
        elif 'python' in item['name'].lower():
            python += 1
        elif 'java' in item['name'].lower():
            java += 1
        elif 'ruby' in item['name'].lower():
            ruby += 1
        elif 'php' in item['name'].lower():
            php += 1
        elif 'cpp' in item['name'].lower():
            cpp += 1
        elif 'swift' in item['name'].lower():
            swift += 1
        elif 'go' in item['name'].lower():
            go += 1

    languages = {
        'javascript': javascript,
        'python': python,
        'java': java,
        'ruby': ruby,
        'php': php,
        'cpp': cpp,
        'swift': swift,
        'go': go
        }

    return languages


def predict_rub_salary(language):
    salary = []
    for item in get_vacancies():
        if language in item['name'].lower():
            if not item['salary']:
                continue
            elif item['salary']['currency'] == 'RUR':
                if item['salary']['from'] and item['salary']['to']:
                   salary.append((item['salary']['from']+item['salary']['to']) / 2)
                elif item['salary']['from']:
                    salary.append(item['salary']['from'] * 1.2)
                elif item['salary']['to']:
                    salary.append(item['salary']['to'] * 0.8)
    return salary


def get_average_salary(language):
    salaries = predict_rub_salary(language)
    if salaries:
        avg_salary = int(mean(salaries))
        return avg_salary
    else:
        return 'Нет данных о зарплате'


def get_processed_vacancies(language):
    salaries = predict_rub_salary(language)
    if salaries:
        return len(salaries)
    else:
        return 'Нет данных о зарплате'


def main():
    languages = {
        'Python': {'vacancies_found': get_programming_language()['python'],
                   'vacancies_processed': get_processed_vacancies('python'),
                   'average_salary': get_average_salary('python')},
        'Java': {'vacancies_found': get_programming_language()['java'],
                   'vacancies_processed': get_processed_vacancies('java'),
                   'average_salary': get_average_salary('java')},
        'JavaScript': {'vacancies_found': get_programming_language()['javascript'],
                   'vacancies_processed': get_processed_vacancies('javascript'),
                   'average_salary': get_average_salary('javascript')},
        'PHP': {'vacancies_found': get_programming_language()['php'],
                   'vacancies_processed': get_processed_vacancies('php'),
                   'average_salary': get_average_salary('php')},
        'Ruby': {'vacancies_found': get_programming_language()['ruby'],
                   'vacancies_processed': get_processed_vacancies('ruby'),
                   'average_salary': get_average_salary('ruby')},
        'C++': {'vacancies_found': get_programming_language()['cpp'],
                   'vacancies_processed': get_processed_vacancies('C++'),
                   'average_salary': get_average_salary('cpp')},
        'Swift': {'vacancies_found': get_programming_language()['swift'],
                   'vacancies_processed': get_processed_vacancies('swift'),
                   'average_salary': get_average_salary('swift')},
        'Go': {'vacancies_found': get_programming_language()['go'],
                   'vacancies_processed': get_processed_vacancies('go'),
                   'average_salary': get_average_salary('go')}
    }

    print(languages)


if __name__ == '__main__':
    main()
