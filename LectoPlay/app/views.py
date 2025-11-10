from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse
# Create your views here.
def home_view(request):
    return render(request , "home.html")

def about_view(request):
    return render(request, 'about.html')

def ejercicios(request):
    return render(request, 'ejercicios.html')

def contacts(request):
    return render(request, 'contacts.html')