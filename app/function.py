import re


def validate(data, **kwargs):
    validator = list()
    if data == '':
        validator.append("「画面項目名」を入力してください")  # Hay chon
    for i in kwargs:
        if i == 'query':
            for j in kwargs[i]:
                if data in j:
                    validator.append("「画面項目名」は既に存在しています。") # da ton tai
                    break
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
                        break
        if i == 'compare':
            if data != kwargs['compare']:
                validator.append('「パスワード（確認」が不正です。')

    return validator

vali_dict = {
    'email' : {
        'format' : '.+@.+(\.).+',
        'max_length' : 15,
        'query' : ''
    },
    'full_name' : {
        'max_length' : 255
    },
    'fullname_kana' : {
        'max_length' : 255,
    },
    'tel' : {
        'max_length' : 14,
        'format' : '[0-9]+-[0-9]+-[0-9]+$'
    },
    'password' : {
        'onebyte' : True,
        'range' : (5,15),
    },
    'persional_email' : {
        'format' : '.+@.+(\.).+',
        'max_length' : 15,
        'query' : ''
    }
}
def check(a,b):
    if a == b:
        return True
    return False
a = validate('sfs@sdf.com', **vali_dict['email'])
print(vali_dict['email']['query'])
