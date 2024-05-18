from django.http import JsonResponse
from cryptomus import Client
from .models import Creator,Support
import json

MERCHANT_UUID = '044feb21-0bdc-4c26-9fd8-f8a7ca120c88'
PAYMENT_KEY = '1P0521ebLUozs8zAW2EOfNreI6DKi8qKeFuQaDWGzug8r3Wz7k32NCEdlzj5QjgaiagUfXisxmOqPND2HebpIfW1nB1aSrbuQg02PHvIxaj5opvEan9S52t92DV7C9bG'

def create_support(request):
    print('request',request.POST)

    if request.method == 'POST':
        creator = request.POST
        amount= request.POST.get('amount','')
        email = request.POST.get('email','')
        creator_id= request.POST.get('creator_id','')

        data = {
            'amount':1.1,
            'currency':'USD',
            'network': 'Tron',
            'order_id': str(support.id),
            'url_return': f'http://127.0.0.1:8000/creators/{creator_id}/',
            'url_success': f'http://127.0.0.1:8000/creators/{creator_id}/success/',
            'url_callback' : f'http://127.0.0.1:8000/creators/{creator_id}/callback/',
            'to_currency' :'USDT',

        }
        payment = Client.payment(PAYMENT_KEY,MERCHANT_UUID)
        result = payment.create(data)
        jsondata = json.loads(result)

        print(result)
        print(result['uuid'])
        print(result['url'])

        uuid= result['uuid']
        url = result['url']

        support.cryptomus_uuid = uuid
        support.save()



        support = Support.objects.create(
            creator_id=creator_id,
            amount=amount,
            email=email,

        )

        
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})
