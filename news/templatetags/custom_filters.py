from django import template


register = template.Library()


CURRENCIES_SYMBOLS = {
   'rub': 'Р',
   'usd': '$',
}


@register.filter()
def currency(value, code='rub'):
   """
   value: значение, к которому нужно применить фильтр
   code: код валюты
   """
   postfix = CURRENCIES_SYMBOLS[code]

   return f'{value} {postfix}'


swear_words = {'редиска': 'р******', 'редиску': 'р******',}

@register.filter()
def censor(value):
   if type(value) != str:
      raise ValueError
   value = value.split()
   count = 0
   for val in value:
      if val.lower() in swear_words.keys():
         value[count] = swear_words[val.lower()]
      count += 1
   return ' '.join(value)
   