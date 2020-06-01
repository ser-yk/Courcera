import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from .models import Item, Review
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        try:
            document = json.loads(request.body)
            validate(document, REVIEW_SCHEMA_ITEM)
            item = Item.objects.create(title=document['title'],
                                       description=document['description'],
                                       price=document['price'])
            return JsonResponse(data={'id': item.pk}, status=201, safe=True)
        except (json.JSONDecodeError, ValidationError) as err:
            return JsonResponse(data={}, status=400, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            document = json.loads(request.body)
            validate(document, REVIEW_SCHEMA_REVIEW)
            try:
                item = Item.objects.get(pk=item_id)
                rev = Review.objects.create(grade=document['grade'], text=document['text'], item=item)
                return JsonResponse(data={'id': rev.pk}, status=201, safe=True)
            except Item.DoesNotExist:
                return JsonResponse(data={}, status=404, safe=False)
        except (json.JSONDecodeError, ValidationError):
            return JsonResponse(data={}, status=400, safe=False)



class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
            reviews = Review.objects.filter(item=item).order_by('-pk')
            count_rev = reviews.count()
        except Item.DoesNotExist:
            return JsonResponse(data={}, status=404, safe=False)

        if count_rev == 0:
            JsonResponse(data={}, status=200, safe=True)

        data = {"id": item_id, "title": item.title, "description": item.description, "price": item.price, "reviews": []}
        if count_rev <= 5:
            pass
        else:
            count_rev = 5
        for review in reviews[:count_rev]:
            rev_data = {"id": review.pk,
                        "text": review.text,
                        "grade": review.grade}
            data['reviews'].append(rev_data)
        return JsonResponse(data=data, status=200, safe=True)


REVIEW_SCHEMA_ITEM = {'$schema': 'http://json-schema.org/schema#',
                      "type": "object",
                      'properties': {"title": {"type": "string", "minLength": 1, "maxLength": 64},
                                     "description": {"type": "string", "minLength": 1, "maxLength": 1024},
                                     "price": {"type": "number", "minimum": 1, "maximum": 1000000}},
                      'required': ["title", "description", "price"]
                      }

REVIEW_SCHEMA_REVIEW = {'$schema': 'http://json-schema.org/schema#',
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "minLength": 1, "maxLength": 1024},
                            "grade": {"type": "number", "minimum": 1, "maximum": 10}},
                        'required': ["text", "grade"]
                        }
