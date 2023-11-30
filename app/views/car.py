from django.views import View
from django.http import HttpRequest, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from app.models import Car,Company
from .company import to_company
import json

def to_dict(car: Car) -> dict:

    return{
            "id":car.pk,
            "company_id":car.company.pk,
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

class CarallView(View):
    def get(self,request:HttpRequest) -> JsonResponse:
    
        try:
            car_all = Car.objects.all()
        except ObjectDoesNotExist:
            return JsonResponse({'result':'object does not exist!'})
            
        result = [to_dict(car) for car in car_all]

        return JsonResponse(result,safe=False)
    
        

class CarView(View):
    def get(self,request:HttpRequest,id = None) -> JsonResponse:
    
        try:
            company = Company.objects.get(id = id)
            car_all = Car.objects.filter(company = company)
        except ObjectDoesNotExist:
            return JsonResponse({'result':'object does not exist!'})
            
        result = [to_dict(car) for car in car_all]

        return JsonResponse(result,safe=False)
        
    def post(self, request:HttpRequest,id ) -> JsonResponse:
        data_json = request.body.decode()
        data = json.loads(data_json)

        company = Company.objects.get(id = id)

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
            company = company,
            name = data['name'],
            url  = data['url'],
            description = data.get('description',''),
            price = data['price'],
            color = data['color'],
            years = data['years'],
            motors = data['motors']
        )

        return JsonResponse(to_dict(car))
    
class CarIDView(View):
    def get(self,request:HttpRequest,id,car_id) -> JsonResponse:
        try:
            company = Company.objects.get(id = car_id)
            car = Car.objects.get(company=company,id=id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'object does not exist!'})
        return JsonResponse(to_dict(car=car))
    
    def put(self,request:HttpRequest,id,car_id) -> JsonResponse:
        try:
            company = Company.objects.get(id = car_id)
            car = Car.objects.get(company=company,id=id)
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
    
    def delete(self,request:HttpRequest,id,car_id) -> JsonResponse:
        try:
            company = Company.objects.get(id = car_id)
            car = Car.objects.get(company=company,id=id)

        except ObjectDoesNotExist:
            return JsonResponse({'status': 'object does not exist!'})
        
        car.delete()

        return JsonResponse({'status':'ok'})
    
def all(request:HttpRequest)->JsonResponse:
    company_all = Company.objects.all()

    result = []
    for company in company_all:
        company_data = to_company(company)
        try:
            company = company_data['id']
            car_all = Car.objects.filter(company = company)
            company_data['car'] = [to_dict(car) for car in car_all]
        except ObjectDoesNotExist:
            company_data['car'] = None
            
        result.append(company_data)

    return JsonResponse({'result':result})
    