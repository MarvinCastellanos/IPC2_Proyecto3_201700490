from django.shortcuts import render, redirect
import requests

# Create your views here.
endpoint = 'http://localhost:5000{}'

def index(request):
    if request.method == 'GET':
        url = endpoint.format('/datos')  # http://localhost:5000/datos
        data = requests.get(url)  # consulta a la API
        context = {
            'data': data.text,
        }
        return render(request, 'index.html', context)
    elif request.method == 'POST':
        docs = request.FILES['document']
        data = docs.read()
        url = endpoint.format('/datos')
        requests.post(url, data)
        return redirect('index')