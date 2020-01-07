def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        salary = int((salary_from + salary_to) / 2)
        return salary
    if salary_from:
        salary = int(salary_from * 1.2)
        return salary
    else:
        salary = int(salary_to * 0.8)
        return salary
 
