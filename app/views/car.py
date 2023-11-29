from django.views import View
from django.http import HttpRequest, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from app.models import Car
import json

def to_dict(car: Car) -> dict:

    return{
            "id":car.pk,
            "name":car.name,
            "url":car.url,
            "description":car.description,
            "price":car.price,
            "color":car.color,
            "years":car.years,
            "motors":car.motors,

            "creates_at":car.created_at,
            "updated_at":car.updated_at
        }

class CarView(View):
    def get(self,request:HttpRequest,id = None) -> JsonResponse:
        if id is not None:
            try:
                car = Car.objects.get(id = id)
                return JsonResponse(to_dict(car))
            except ObjectDoesNotExist:
                return JsonResponse({'result':'object does not exist!'})
            
        else:
            cars_all = Car.objects.all()

            query_params = request.GET
            name = query_params.get('name')
            if name is not None:
                car = Car.objects.filter(name = name)
            else:
                cars_all = Car.objects.all()
            result = [to_dict(car) for car in cars_all]
            return JsonResponse({'result':result})
        
    def post(self, request:HttpRequest) -> JsonResponse:
        data_json = request.body.decode()
        data = json.loads(data_json)

        if not data.get('name'):
            return JsonResponse({'status': 'name is required!'})
        elif not data.get('url'):
            return JsonResponse({'status': 'url is required!'})
        elif not data['url'].startswith('https://'):
            return JsonResponse({'status': 'url is invalid!'})
        elif not data.get('price'):
            return JsonResponse({'status': 'price is required!'})
        elif not data.get('color'):
            return JsonResponse({'status': 'color is required!'})
        elif not data.get('years'):
            return JsonResponse({'status': 'years is required!'})
        elif not data.get('motors'):
            return JsonResponse({'status': 'motors is required!'})
        
        car = Car.objects.create(
            name = data['name'],
            url  = data['url'],
            description = data.get('description',''),
            price = data['price'],
            color = data['color'],
            years = data['years'],
            motors = data['motors']
        )

        car.save()

        return JsonResponse(to_dict(car))
    
    def put(self, request:HttpRequest,id = None) -> JsonResponse:
        try:
            car = Car.objects.get(id = id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'object does not exist!'})
        
        data_json = request.body.decode()
        data = json.loads(data_json)

        if data.get('name'):
            car.name = data['name']
        if data.get('url'):
            car.url = data['url']
        if data.get('description'):
            car.description = data['description']
        if data.get('price'):
            car.price = data['price']
        if data.get('color'):
            car.color = data['color']
        if data.get('years'):
            car.years = data['years']
        if data.get('motors'):
            car.motors = data['motors']

        car.save()

        return JsonResponse(to_dict(car=car))
    
    def delete(self, request:HttpRequest,id = None) -> JsonResponse:
        try:
            car = Car.objects.get(id = id)

        except ObjectDoesNotExist:
            return JsonResponse({'status': 'object does not exist!'})
        
        car.delete()

        return JsonResponse({'status':'ok'})
    
    