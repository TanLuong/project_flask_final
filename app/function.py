import re
from  math import ceil
def validate(name, data, **kwargs):

    if data in kwargs['require']:
        return 'exist'
    if data not in kwargs['not_require']:
        return 'not exist'
    if len(data) > kwargs['length']:
        return 'Khong duoc vuot qua' + str(kwargs['length'])
