import re
from  math import ceil

from werkzeug.datastructures import TypeConversionDict

def validate(data, **kwargs):
    validator = list()
    if data == '':
        validator.append("「画面項目名」を入力してください")  # Hay chon
    for i in kwargs:
        if i == 'query':
            if data in kwargs['query']:
                validator.append("「画面項目名」は既に存在しています。") # da ton tai
        if i == 'format':
            if not re.findall(kwargs['format'], data):
                validator.append(f"「画面項目名」を{kwargs['format']}形式で入力してください") # sai format
        if i == 'maxlength':
            if len(data) >= kwargs['maxlength']:
                validator.append(f"{kwargs['maxlength']}桁以内の「画面項目名」を入力してください") # nho hon maxlength
        if i == 'range':
            if (len(data) <= kwargs['range'][0]) or (len(data) >= kwargs['range'][1]):
                validator.append(f"「画面項目名」を{kwargs['range'][0]}＜＝桁数、＜＝{kwargs['range'][1]}桁で入力してください") # trong khoang
        if i == 'onebyte':
            if kwargs['onebyte'] == True:
                for j in data:
                    if ord(j) > 255:
                        validator.append('「画面項目名」に半角英数を入力してください')
        # if i == 'compare':

    return validator

def check(a,b):
    if a == b:
        return True
    return False

a = validate('0386-556-225', format='[0-9]{4}-[0-9]{3}-[0-9]{3}$' )
print(a)
