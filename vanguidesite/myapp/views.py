# myapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

@csrf_exempt
def process_input(request, **kwargs):
    if request.method == 'POST':
        input_data1 = request.POST.get('input_data1', '')
        input_data2 = request.POST.get('input_data2', '')
        print(f'Input 1 from the user: {input_data1}')
        print(f'Input 2 from the user: {input_data2}')
        return JsonResponse({'message': f'Input received successfully: {input_data1, input_data2}'})

    location_data = kwargs.get('location_data', '')
    destination_data = kwargs.get('destination_data', '')
    if location_data != '' and destination_data != '':
        return render(request, 'myapp/index.html', {'input_data1': location_data, 'input_data2': destination_data})
    elif location_data != '':
        return render(request, 'myapp/index.html', {'input_data1': location_data})
    elif destination_data != '':
        return render(request, 'myapp/index.html', {'input_data2': destination_data})

def index(request):
    return render(request, 'myapp/index.html', {})