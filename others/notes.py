import json

price_fruits = dict(apple=100, orange=90, grape=120)

price_fruits_json = json.dumps(price_fruits)


print(price_fruits)
print(type(price_fruits))

print(price_fruits_json)
print(type(price_fruits_json))

