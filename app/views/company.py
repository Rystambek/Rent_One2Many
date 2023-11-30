from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from app.models import Company
import json


def to_company(company:Company) -> dict:

    return {
        "id":company.pk,
        "name":company.name,
        "website":company.website
    }

class CompanyView(View):
    def get(self, request:HttpRequest,id = None) -> JsonResponse:
        if id is not None:
            try:
                company = Company.objects.get(id = id)
                return JsonResponse(to_company(company))
            except ObjectDoesNotExist:
                return JsonResponse({'result':'object does not exist!'})
            
        else:
            company_all = Company.objects.all()

            result = [to_company(company) for company in company_all]
            return JsonResponse(result,safe=False)
    
    def post(self,request:HttpRequest,id = None) -> JsonResponse:

        data_json = request.body.decode()
        data = json.loads(data_json)

        if not data.get('name'):
            return JsonResponse({'status': 'name is required!'})
        elif not data.get('website'):
            return JsonResponse({'status': 'website is required!'})

        if id is not None:
            company = Company.objects.create(
                pk = id,
                name = data['name'],
                website = data['website']
            )

        else:

            company = Company.objects.create(
                name = data['name'],
                website = data['website']
            )

            company.save()
            return JsonResponse({'result':to_company(company)})
        
    def put(self, request:HttpRequest,id = None) -> JsonResponse:
        try:
            company = Company.objects.get(id = id)

        except ObjectDoesNotExist:
            return JsonResponse({'status': 'object does not exist!'})
        
        data_json = request.body.decode()
        data = json.loads(data_json)

        if data.get('name'):
            company.name = data['name']
        if data.get('website'):
            company.website = data['website']

        company.save()

        return JsonResponse(to_company(company))
    
    def delete(self,request:HttpRequest, id = None) -> JsonResponse:
        try:
            company = Company.objects.get(id = id)

        except ObjectDoesNotExist:
            return JsonResponse({'status': 'object does not exist!'})
        
        company.delete()

        return JsonResponse({'status':"Ok"})
    
