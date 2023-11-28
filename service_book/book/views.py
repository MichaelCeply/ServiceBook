from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from functools import wraps
from django.contrib.auth.decorators import login_required
from .models import Record,Person,Car,Section
from .forms import RecordForm

# Create your views here.

def session_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('authenticated'):
            return view_func(request, *args, **kwargs)
        else:
            # Redirect to a login page or some unauthorized page
            return redirect('password')  # Adjust this to your login view
    return wrapper

@session_login_required
def index(request):
    # Get filter parameters from the GET request
    car_filter = request.GET.get('car')
    person_filter = request.GET.get('person')
    section_filter = request.GET.get('section')
    time_from = request.GET.get('time_from')
    time_to = request.GET.get('time_to')

    # Start with all records
    records = Record.objects.order_by('-datetime')

    # Apply filters if they are provided
    if car_filter:
        records = records.filter(car__id=car_filter)
    if person_filter:
        records = records.filter(person__id=person_filter)
    if section_filter:
        records = records.filter(section__id=section_filter)
    if time_from:
        records = records.filter(datetime__gte=time_from)
    if time_to:
        records = records.filter(datetime__lte=time_to)

    # Query for cars, persons, and sections
    cars = Car.objects.order_by('name')
    persons = Person.objects.order_by('login')
    sections = Section.objects.order_by('name')

    return render(request, 'index.html', {'records': records, 'cars': cars, 'persons': persons, 'sections': sections})

@session_login_required
def new_record(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to a success page or another view
    else:
        form = RecordForm()
    return render(request, 'new_record.html', {'form': form})

def password_check(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        
        # Hardcoded password for demonstration (replace this with your actual password)
        hardcoded_password = '12345'
        
        if password == hardcoded_password:
            # Password matches, consider the user authenticated
            request.session['authenticated'] = True  # Using session for authentication
            print("ok")
            return redirect('index')  # Redirect to a success page
        else:
            # Authentication failed, show an error
            error_message = "Invalid password. Please try again."
            return render(request, 'password.html', {'error': error_message})

    return render(request, 'password.html')

def logout(request):
    if 'authenticated' in request.session:
        del request.session['authenticated']
    # Optionally, you might want to clear the entire session
    request.session.flush()
    return redirect('password')  # Redirect to your login page after logout
