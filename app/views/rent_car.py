from django.views import View
from django.http import HttpRequest, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from app.models import Rent_car,Car
from .car import to_dict
import json

def to_rent(rent:Rent_car) -> dict:

    return {
        'id':rent.pk,
        'car_id':rent.car.pk,
        'rent_number':rent.rent_number,
        'car_number':rent.car_number,
        'car_yoqilgi':rent.car_yoqilgi,
        'model':rent.model
    }

class RentView(View):
    def get(self,request:HttpRequest,id) -> JsonResponse:
        try:
            car = Car.objects.get(id = id)
            rent = Rent_car.objects.get(car = car)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'object does not exist!'})

        return JsonResponse(to_rent(rent))

    def post(self,request:HttpRequest,id) -> JsonResponse:
        data_json = request.body.decode()
        data = json.loads(data_json)

        car = Car.objects.get(id = id)

        if not data.get('rent_number'):
            return JsonResponse({'status': 'rent_number is required!'})
        elif not data.get('car_number'):
            return JsonResponse({'status': 'car_number is required!'})
        elif not data.get('car_yoqilgi'):
            return JsonResponse({'status': 'car_yoqilgi is required!'})
        elif not data.get('model'):
            return JsonResponse({'status': 'model is required!'})
        
        rent = Rent_car.objects.create(
            car_id = car.pk,
            rent_number = data['rent_number'],
            car_number = data['car_number'],
            car_yoqilgi = data['car_yoqilgi'],
            model = data['model']
        )

        rent.save()
        return JsonResponse(to_rent(rent))
    
    def put(self, request:HttpRequest,id) -> JsonResponse:
        try:
            car = Car.objects.get(id = id)
            rent = Rent_car.objects.get(car = car)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'object does not exist!'})
        
        data_json = request.body.decode()
        data = json.loads(data_json)

        if data.get('rent_number'):
            rent.rent_number = data['rent_number']
        if data.get('car_number'):
            rent.car_number = data['car_number']
        if data.get('car_yoqilgi'):
            rent.car_yoqilgi = data['car_yoqilgi']
        if data.get('model'):
            rent.model = data['model']

        rent.save()

        return JsonResponse(to_rent(rent))
    
    def delete(self, request:HttpRequest,id) -> JsonResponse:
        try:
            car = Car.objects.get(id = id)
            rent = Rent_car.objects.get(car = car)

        except ObjectDoesNotExist:
            return JsonResponse({'status': 'object does not exist!'})
        
        rent.delete()

        return JsonResponse({'status':'ok'})
    
def all(request:HttpRequest)->JsonResponse:
    car_all = Car.objects.all()

    result = []
    for car in car_all:
        car_data = to_dict(car)
        try:
            rent = Rent_car.objects.get(car = car)
            car_data['rent'] = to_rent(rent)
        except ObjectDoesNotExist:
            car_data['rent'] = None
            
        result.append(car_data)

    return JsonResponse({'result':result})
