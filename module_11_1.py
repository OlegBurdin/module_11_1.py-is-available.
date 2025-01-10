import requests
import pandas
from pprint import pprint

URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

"""
Использование модуля requests.
Получить данные о курсах валют с сайта на текущую дату и записать 
полученные данные в переменную r в формате json.
"""

r = requests.get(URL)
json_flag = False
if r.ok:
    try:
        r = r.json()
    except requests.exceptions.JSONDecodeError as e:
        print('Содержимое ответа не в формате json.', 'От источника был получен следующий ответ:',
              r, sep='\n')
    else:
        json_flag = True
pprint(r['Valute'])

"""
Использование модуля pandas.
Сохранить полученные курсы валют в файле .xlsx.
"""

if json_flag:
    # Формируем список валют для записи в файл
    field_list = ['CharCode', 'NumCode', 'Name', 'Nominal', 'Value']
    val_list = []
    for i in r['Valute']:
        line_ = []
        for j in field_list:
            line_.append(r['Valute'][i][j])
        val_list.append(line_)

    val_list.sort(key=lambda x: -x[3])
    pprint(val_list)

    # Сохраняем полученные данные в файл .xlsx
    df1 = pandas.DataFrame(val_list, columns=field_list)
    with pandas.ExcelWriter(f"val_{r['Date'][0:10]}.xlsx") as writer:
        df1.to_excel(writer, sheet_name=str(r['Date'][0:10]))

