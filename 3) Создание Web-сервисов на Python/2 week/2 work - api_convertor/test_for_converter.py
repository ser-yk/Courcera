import requests
from decimal import Decimal

# Необходимо имортировать конвертор convert


correct = Decimal('3754.8057')
result = convert(Decimal("1000.1000"), 'RUR', 'JPY', "17/02/2005", requests)
print(result)
if result == correct:
    print("Correct")
else:
    print("Incorrect: %s != %s" % (result, correct))
