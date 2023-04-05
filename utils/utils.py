def get_hh_from_url(url):
    return 'hh' in url


def get_superjob_from_url(url):
    return 'superjob' in url


def get_correct_sj_salary(payment_from, payment_to):
    """ Функция приводящая полученное поле зп к общему шаблонну"""
    correct_data = ''
    empty_salary = 'не указана'
    if payment_from == '0':
        pass
    else:
        correct_data += f'от {payment_from} '
    if payment_to == '0':
        pass
    else:
        correct_data += f'до {payment_to}'
    return correct_data if correct_data else empty_salary


def correct_hh_salary(value_from, value_to):
    """ Функция приводящая полученное поле зп к общему шаблонну"""
    correct_salary_from, correct_salary_to = '', ''
    if value_from != 'None':
        correct_salary_from += 'от ' + value_from
    if value_to != 'None':
        correct_salary_to += 'до ' + value_to
    if correct_salary_from and correct_salary_to:
        return f'{correct_salary_from} {correct_salary_to}'
    elif correct_salary_from or correct_salary_to:
        return f'{correct_salary_from}{correct_salary_to}'


def get_correct_experience_sj(experience):
    """ Функция проводящая поле опыта работы к формату HH"""
    correct_experience = ''
    if experience == 'От 3 лет':
        experience = 'От 3'
        correct_experience += experience + ' до 6 лет'
    elif experience == 'От 1 года':
        correct_experience += experience + ' до 3 лет'
    else:
        correct_experience += 'Без опыта'
    return correct_experience