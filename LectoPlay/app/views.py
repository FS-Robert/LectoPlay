from django.shortcuts import render, redirect
from firebase_admin import auth

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

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )
        return redirect('login')
    return render(request, 'register.html')



def login_view(request):
    return render(request, 'login.html')