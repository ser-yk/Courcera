import json

data = {
    "id": 2,
    "title": 'item.title',
    "description": 'item.description',
    "price": 'item.price',
    "reviews": {"id": 'review', "text": 'review', "grade": 'grade'}
}
a = json.dumps(data)
print(json.dumps(data))
print(type(data['id']))