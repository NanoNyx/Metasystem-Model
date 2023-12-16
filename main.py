import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
import sys
import pandas as pd

# -----------------КРОК 1 ----------------- 
# ІНІЦІАЛІЗАЦІЯ ФУНКЦІЙ ЗІ СТАНДАРТНИМИ MIN/MAX ЗНАЧЕННЯМИ ПАРАМЕТРІВ 

# Стандартний пульс
def min_max_pulse(age):
    if age <= 1:
        min_val, max_val = (70, 190)
    elif age <= 2:
        min_val, max_val = (80, 130)
    elif age <= 4:
        min_val, max_val = (80, 120)
    elif age <= 6:
        min_val, max_val = (75, 115)
    elif age <= 9:
        min_val, max_val = (70, 110)
    else:
        min_val, max_val = (60, 100)
    return min_val, max_val

# Стандартний артеріальний тиск
def min_max_blood_pressure(age):
    if age <= 1:
        min_val, max_val = (75, 100)
    elif age <= 9:
        min_val, max_val = (90, 110)
    else:
        min_val, max_val = (90, 120)
    return min_val, max_val

# Стандартна ЕКГ(Електрокардіографія)
def min_max_ecg(age):
    if age <= 1:
        min_val, max_val = (80, 150)
    elif age <= 21:
        min_val, max_val = (80, 180)
    else:
        min_val, max_val = (120, 200)
    return min_val, max_val

# Стандартна сатурація
def min_max_oxygen_saturation(age):
    if age <= 150:
        min_val, max_val = (98, 100)
    return min_val, max_val

# Стандартний рівень холестерину в крові 
def min_max_cholesterol(age):
    if age <= 19:
        min_val, max_val = (40, 170)
    else:
        min_val, max_val = (125, 200)
    return min_val, max_val

# Стандартний рівень цукру в крові 
def min_max_blood_sugar(age):
    if age <= 150:
       min_val, max_val = (70, 100)
       return min_val, max_val


# -----------------КРОК 2 ----------------- 
#СТВОРЕННЯ СИСТЕМИ(класу) ДЛЯ ІНІЦІАЛІЗАЦІЇ ОСОБИСТИХ ДАНИХ ПАЦІЄНТА +
# + ФУНКЦІЯ ВИПАДКОВИХ ЗНАЧЕНЬ З ТЕСТОВИМИ ДАНИМИ  

# Створення системи S_1 (особисті дані пацієнта)
class SystemS1:
    def __init__(self):
        self.patients = []

    def add_patient(self, patient):
        self.patients.append(patient)

    def compare_results(self, patient_id):
        patient_s1 = next((patient for patient in self.patients if patient.id == patient_id), None)

        if patient_s1:
            if patient_s1.has_violations:
                print(f"Пацієнт {patient_id} має порушення в системі S_1.")
            else:
                print(f"Пацієнт {patient_id} не має порушень в системі S_1.")
        else:
            print(f"Пацієнт з ID {patient_id} не знайдений.")

# Функція для генерації тестових даних пацієнта
def generate_test_patient():
    age = np.random.randint(0.1, 120)
    gender = np.random.choice(['чоловік', 'жінка'])

    initial_results = {
        'pulse': int(np.random.randint(60, 190)),
        'systolic_bp': int(np.random.randint(60, 190)),
        'diastolic_bp': int(np.random.randint(50, 120)),
        'pr_interval': int(np.random.uniform(80, 200)),
        'saturation_level': int(np.random.uniform(95, 100)),
        'total_chol': int(np.random.randint(50, 240)),
        'fasting_glucose': int(np.random.uniform(70, 200)),
    }

    repeated_results = {param: int(value + np.random.uniform(-1, 1)) for param, value in initial_results.items()}

    return age, gender, initial_results, repeated_results    

# -----------------КРОК 3 ----------------- 
#СТВОРЕННЯ СИСТЕМИ(класу) ДЛЯ ІНІЦІАЛІЗАЦІЇ РЕЗУЛЬТАТІВ ПОЧАТКОВИХ АНАЛІЗІВ ПАЦІЄНТА

# Створення системи S_2 (результати початкових аналізів)
class SystemS2:
    def __init__(self, system_s1):
        self.system_s1 = system_s1
        self.patients = []

    def add_patient(self, patient):
        self.system_s1.add_patient(patient)
        self.patients.append(patient)

    def compare_results(self, patient_id):
        self.system_s1.compare_results(patient_id)


# -----------------КРОК 4 -----------------
#СТВОРЕННЯ СИСТЕМИ(класу) ДЛЯ ІНІЦІАЛІЗАЦІЇ РЕЗУЛЬТАТІВ ПОВТОРНИХ АНАЛІЗІВ ПАЦІЄНТА

# Створення системи S_3
class SystemS3:
    def __init__(self, system_s2):
        self.system_s2 = system_s2
        self.patients = []

    def add_patient(self, patient):
        self.system_s2.add_patient(patient)
        self.patients.append(patient)

    def compare_results(self, patient_id):
        self.system_s2.compare_results(patient_id)


# -----------------КРОК 5 -----------------
#СТВОРЕННЯ СИСТЕМИ З ПОЄДНАННЯМ ПОПЕРЕДНІХ КЛАСІВ ДЛЯ УТВОРЕННЯ ЦІЛЬНОГО ОБРАЗУ ПАЦІЄНТА

# Створення СИСТЕМИ Patient
class Patient:
    def __init__(self, id, name, age, gender, initial_results=None, repeated_results=None):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.initial_results = initial_results if initial_results is not None else {}
        self.repeated_results = repeated_results if repeated_results is not None else {}
        self.has_violations = False

    def add_initial_results(self, results):
        self.initial_results = results

    def add_repeated_results(self, results):
        self.repeated_results = results

    def display_results(self):
        print(f"Результати аналізів пацієнта {self.name} (ID: {self.id}):\n")
        print("Початкові аналізи:", self.initial_results, "\n")
        print("Повторні аналізи:", self.repeated_results, "\n")

# -----------------КРОК 6 -----------------
#ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ КОРЕКТНОЇ РОБОТИ МЕТАСИСТЕМИ

# Функція для введення числового значення з перевіркою на коректність
def input_numeric_value(prompt, min_value=float('-inf'), max_value=float('inf')):
    while True:
        try:
            value = float(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                confirm = input(f"Ви впевнені, що ввели правильне значення ({min_value} - {max_value})? (так/ні): ")
                if confirm.lower() == 'так':
                    return value
        except ValueError:
            print("Будь ласка, введіть числове значення.")

# Функція для введення даних пацієнта
def input_patient():
    patient_id = input_numeric_value("Введіть ID пацієнта: ", 0)
    patient_name = input("Введіть ім'я пацієнта: ")
    patient_age = input_numeric_value("Введіть вік пацієнта: ")
    patient_gender = input("Введіть стать пацієнта (чоловік/жінка): ")

    return Patient(id=patient_id, name=patient_name, age=patient_age, gender=patient_gender) 


# Функція для введення початкових аналізів
def input_initial_results(patient):
    patient_data = {
        'pulse': input_numeric_value("Введіть пульс: "),
        'systolic_bp': input_numeric_value("Введіть систолічний тиск: "),
        'diastolic_bp': input_numeric_value("Введіть діастолічний тиск: "),
        'pr_interval': input_numeric_value("Введіть інтервал PR: "),
        'saturation_level': input_numeric_value("Введіть рівень насичення киснем: ", 0, 100),
        'total_chol': input_numeric_value("Введіть загальний холестерин: "),
        'fasting_glucose': input_numeric_value("Введіть рівень глюкози натщесерце: "),
    }

    patient.add_initial_results(patient_data)

# Функція для введення повторних аналізів
def input_repeated_results(patient):
    repeated_results = {
        'pulse': input_numeric_value("Введіть повторний пульс: "),
        'systolic_bp': input_numeric_value("Введіть повторний систолічний тиск: "),
        'diastolic_bp': input_numeric_value("Введіть повторний діастолічний тиск: "),
        'pr_interval': input_numeric_value("Введіть повторний інтервал PR: "),
        'saturation_level': input_numeric_value("Введіть повторний рівень насичення киснем: ", 0, 100),
        'total_chol': input_numeric_value("Введіть загальний холестерин: "),
        'fasting_glucose': input_numeric_value("Введіть повторний рівень глюкози натщесерце: "),
    }

    patient.add_repeated_results(repeated_results)

# -----------------КРОК 6 -----------------
#ПОРІВНЯННЯ В НОВІЙ СИСТЕМІ(класі) РЕЗУЛЬТАТІВ ПОЧАТКОВИХ ТА ПОВТОРНИХ 
# АНАЛІЗІВ ПАЦІЄНТА, ПОШУК % ВІДХИЛЕНЬ ВІД MIN/MAX

#Створення системи S_4 
class SystemS4:
    def __init__(self, system_s3, system_s2):
        self.system_s3 = system_s3
        self.system_s2 = system_s2

    def compare_results(self, patient_id):
        patient_s3 = next((patient for patient in self.system_s3.patients if patient.id == patient_id), None)
        patient_s2 = next((patient for patient in self.system_s2.patients if patient.id == patient_id), None)

        if patient_s3 and patient_s2:
            # Перший крок: розрахунок середнього значення для кожного параметра
            average_results = {}
            parameters = [
                'pulse', 'systolic_bp', 'diastolic_bp', 'pr_interval', 'saturation_level',
                'total_chol', 'fasting_glucose'
            ]

            for param in parameters:
                average_results[param] = (patient_s3.initial_results[param] + patient_s3.repeated_results[param]) / 2

            # Другий крок: порівняння результатів з функціями min_max_...
            for param in parameters:
                if param == 'pulse':
                   min_val, max_val = min_max_pulse(patient_s3.age)
                elif param in ['systolic_bp', 'diastolic_bp']:
                    min_val, max_val = min_max_blood_pressure(patient_s3.age)
                elif param == 'pr_interval':
                   min_val, max_val = min_max_ecg(patient_s3.age)
                elif param == 'saturation_level':
                   min_val, max_val = min_max_oxygen_saturation(patient_s3.age)
                elif param == 'total_chol':
                   min_val, max_val = min_max_cholesterol(patient_s3.age)
                elif param == 'fasting_glucose':
                   min_val, max_val = min_max_blood_sugar(patient_s3.age)

                if min_val <= average_results[param] <= max_val:
                    deviation_percentage = 0
                elif average_results[param] > max_val:
                    deviation_percentage = ((average_results[param] - max_val) / max_val) * 100
                elif average_results[param] < min_val:
                    deviation_percentage = ((average_results[param] - min_val) / min_val) * 100

                print(f"% Відхилення для {param}: {deviation_percentage:.2f}%")

        else:
            print(f"Пацієнт з ID {patient_id} не знайдений в одній з систем (S_3 або S_2).")


# -----------------КРОК 7 -----------------
#ПОБУДОВА ГРАФІКУ, ЩО ПІДСУМОВУЄ ДАНІ, ВІДОБРАЖАЮЧИ СТАН ПАЦІЄНТА

import matplotlib.pyplot as plt
import numpy as np

# Графік
def plot_results(patient):
    parameters = [
        'pulse', 'systolic_bp', 'diastolic_bp', 'pr_interval', 'saturation_level',
        'total_chol', 'fasting_glucose'
    ]

    categories = list(range(len(parameters)))
    initial_results = [patient.initial_results[param] for param in parameters]
    repeated_results = [patient.repeated_results[param] for param in parameters]

    normal_ranges = []

    for param in parameters:
        normal_range = None
        if param == 'pulse':
            normal_range = min_max_pulse(patient.age)
        elif param in ['systolic_bp', 'diastolic_bp']:
            normal_range = min_max_blood_pressure(patient.age)
        elif param == 'pr_interval':
            normal_range = min_max_ecg(patient.age)
        elif param == 'saturation_level':
            normal_range = min_max_oxygen_saturation(patient.age)
        elif param == 'total_chol':
            normal_range = min_max_cholesterol(patient.age)
        elif param == 'fasting_glucose':
            normal_range = min_max_blood_sugar(patient.age)

        normal_ranges.append(normal_range)

    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.35
    bar_width = width / 2

    # Стовпчики для початкових і повторних аналізів
    bars1 = ax.bar(np.array(categories) - bar_width, initial_results, width=bar_width, label='Початкові аналізи')
    bars2 = ax.bar(np.array(categories) + bar_width, repeated_results, width=bar_width, label='Повторні аналізи', alpha=0.5)

    for i, param in enumerate(parameters):
        normal_range = normal_ranges[i]
        if param == 'pulse':
            ax.fill_between([i - bar_width, i + bar_width], normal_range[0], normal_range[1], color='green', alpha=0.1, label='Пульс')
        elif param in ['systolic_bp', 'diastolic_bp']:
            ax.fill_between([i - bar_width, i + bar_width], normal_range[0], normal_range[1], color='pink', alpha=0.2, label='Тиск')
        elif param == 'pr_interval':
            ax.fill_between([i - bar_width, i + bar_width], normal_range[0], normal_range[1], color='purple', alpha=0.2, label='Інтервал PR')
        elif param == 'saturation_level':
            ax.fill_between([i - bar_width, i + bar_width], normal_range[0], normal_range[1], color='red', alpha=0.2, label='Рівень насичення киснем')
        elif param == 'total_chol':
            ax.fill_between([i - bar_width, i + bar_width], normal_range[0], normal_range[1], color='yellow', alpha=0.2, label='Холестерин')
        elif param == 'fasting_glucose':
            ax.fill_between([i - bar_width, i + bar_width], normal_range[0], normal_range[1], color='black', alpha=0.2, label='Глюкоза натще')

    ax.set_xticks(categories)
    ax.set_xticklabels(parameters)
    ax.set_yticks(range(0, 210, 10))  # діапазон
    ax.set_ylabel('Значення параметрів')
    ax.set_title(f'Результати аналізів пацієнта {patient.name} (ID: {patient.id})\nВік: {patient.age}, Гендер: {patient.gender}')
    
    # Додавання числових значень над стовпцями
    for i, value in enumerate(initial_results):
        ax.text(i - bar_width, value + 2, f'{value:.2f}', ha='center', va='bottom', color='black', fontsize=8)
    
    for i, value in enumerate(repeated_results):
        ax.text(i + bar_width, value + 2, f'{value:.2f}', ha='center', va='bottom', color='black', fontsize=8)

    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.show()





# -----------------КРОК 8 -----------------
# ДОДАВАННЯ МОЖЛИВОСТІ ВИБРАТИ СПОСІБ ВВОДУ З КОНСОЛІ

# Функція для вибору введення даних: з консолі чи тестових даних
def choose_input_method():
    while True:
        sys.stdout.write("Бажаєте ввести дані самостійно чи скористатися тестовими даними? (введіть 'консоль' або 'тест'): ")
        sys.stdout.flush()

        input_method = sys.stdin.readline().strip().lower()

        if input_method in ['консоль', 'тест']:
            return input_method
        else:
            sys.stdout.write("Неправильний ввід. Будь ласка, введіть 'консоль' або 'тест'.\n")
            sys.stdout.flush()

# -----------------КРОК 9 -----------------
def save_to_excel(patient_data, file_name):
    # Завантаження існуючого файлу, якщо він існує
    try:
        existing_df = pd.read_excel('d:/patient_data.xlsx')
    except FileNotFoundError:
        existing_df = pd.DataFrame()

    data = {
        '№': [patient_data.id],
        'Ф.І.О.': [patient_data.name],
        'Вік': [patient_data.age],
        'Стать': [patient_data.gender],
        '1-Пульс': [patient_data.initial_results['pulse']],
        '1-Сист.тиск': [patient_data.initial_results['systolic_bp']],
        '1-Дист.тиск': [patient_data.initial_results['diastolic_bp']],
        '1-ЕКГ': [patient_data.initial_results['pr_interval']],
        '1-Сатурація': [patient_data.initial_results['saturation_level']],
        '1-Заг.холестерин': [patient_data.initial_results['total_chol']],
        '1-Глюкоза': [patient_data.initial_results['fasting_glucose']],
        '2-Пульс': [patient_data.repeated_results['pulse']],
        '2-Сист.тиск': [patient_data.repeated_results['systolic_bp']],
        '2-Дист.тиск': [patient_data.repeated_results['diastolic_bp']],
        '2-ЕКГ': [patient_data.repeated_results['pr_interval']],
        '2-Сатурація': [patient_data.repeated_results['saturation_level']],
        '2-Заг.холестерин': [patient_data.repeated_results['total_chol']],
        '2-Глюкоза': [patient_data.repeated_results['fasting_glucose']]
    }

    df = pd.DataFrame(data)

    # Додати новий рядок до існуючого DataFrame
    updated_df = pd.concat([existing_df, df], ignore_index=True)

    # Зберегти оновлений DataFrame у файл
    updated_df.to_excel('d:/patient_data.xlsx', index=False)

# -----------------КРОК 10 -----------------
# ОСНОВНА ЧАСТИНА ПРОГРАМИ

def main():

    while True:
        print("Дослідження роботи серця:\n\n")

        # Створення системи S_1
        print("Дані пацієнта:\n")
      #  sys.stdout.flush()

        input_method = choose_input_method()

        if input_method == 'консоль':
            patient_s1 = input_patient()
            system_s1 = SystemS1()
            system_s1.add_patient(patient_s1)
            
        else:  # використання тестових даних
            age, gender, initial_results, repeated_results = generate_test_patient()
            patient_s1 = Patient(id=1, name='Тестовий Пацієнт', age=age, gender=gender,
                                 initial_results=initial_results, repeated_results=repeated_results)
            system_s1 = SystemS1()
            system_s1.add_patient(patient_s1)

        # Створення системи S_2 та введення даних пацієнта та результатів аналізів
        print("\nПочаткові аналізи:\n")
        sys.stdout.flush()

        system_s2 = None
        if input_method == 'консоль':
            input_initial_results(patient_s1)
            system_s2 = SystemS2(system_s1)  # Додайте цей рядок
        else:  # використання тестових даних
            age, gender, initial_results, repeated_results = generate_test_patient()
            patient_s1.add_initial_results(initial_results)

            system_s2 = SystemS2(system_s1)
            system_s2.add_patient(patient_s1)

        # Створення системи S_3 та введення даних пацієнта та результатів повторних аналізів
        print("\nПовторні аналізи:\n")
        sys.stdout.flush()

        if input_method == 'консоль':
            input_repeated_results(patient_s1)
        else:  # використання тестових даних
            age, gender, initial_results, repeated_results = generate_test_patient()
            patient_s1.add_repeated_results(repeated_results)

        system_s3 = SystemS3(system_s2)
        system_s3.add_patient(patient_s1)
        patient_s1.display_results()

        # Створення системи S_4 та порівняння результатів
        system_s4 = SystemS4(system_s3, system_s2)
        patient_id = int(input("Введіть ID пацієнта для порівняння результатів між S_3 та S_2: "))
        system_s4.compare_results(patient_id)

        # Виклик функції для відображення графіку результатів
        plot_results(patient_s1)

        # Зберегання даних поточного користувача у файл
        save_to_excel(patient_s1, 'patient_data.xlsx')

        # Запит у користувача
        sys.stdout.write("\nБажаєте продовжити дослідження? (так/ні): ")
        sys.stdout.flush()
        continue_research = sys.stdin.readline().strip().lower()

        if continue_research != 'так':
            break

if __name__ == "__main__":
    main()


