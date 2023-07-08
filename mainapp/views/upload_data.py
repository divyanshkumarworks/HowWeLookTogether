from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from mainapp.models import Data
from django.http import JsonResponse, HttpResponse
from . import maskrun
from .variables import ID
from .maskrun import maskrun_program

import threading
import json

@csrf_exempt
def upload_data_api(request):
	if request.method == "POST"  and 'image1' in request.FILES and 'image2' in request.FILES:

		person1 = request.FILES['image1']
		person2 = request.FILES['image2']
		
		data = request.POST.get("data")
		print(data)
		dic = json.loads(data)
		realh1 = dic.get("height1")
		realh2 = dic.get("height2")

		data = Data(person1=person1, person2=person2, height1=realh1, height2=realh2)
		data.save()

		data_id = data.id

		t = threading.Thread(target=maskrun_program, args=(data_id,))

	    # Start the thread
		t.start()

		return JsonResponse({"order_id": data_id})
	else:
		return JsonResponse({'error': 'not found'}, status=404)

