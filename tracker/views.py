from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm  # Added for Sign Up
from django.contrib import messages  # For success notifications
from .models import Milestone
import json

# --- AUTHENTICATION VIEWS ---

def signup_page(request):
    """View to allow new users (like your supervisor) to create an account."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'tracker/signup.html', {'form': form})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'tracker/login.html', {'error': 'Wrong username or password!'})
    
    return render(request, 'tracker/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# --- MAIN PAGES ---

@login_required(login_url='/login/')
def home_page(request):
    return render(request, 'tracker/index.html')

@login_required(login_url='/login/')
def profile_page(request):
    return render(request, 'tracker/profile.html')

# --- API ENDPOINTS ---

@login_required(login_url='/login/')
def milestone_list_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Milestone.objects.create(
            title=data['title'],
            category=data.get('category', 'General'),
            description=data.get('description', ''),
            status=data.get('status', 'planned')
        )
        return JsonResponse({'status': 'success'})

    milestones = Milestone.objects.all().values('id', 'title', 'category', 'description', 'status', 'date_created', 'date_updated')
    return JsonResponse(list(milestones), safe=False)

@login_required(login_url='/login/')
def delete_milestone_api(request, pk):
    if request.method == 'POST':
        try:
            milestone = Milestone.objects.get(pk=pk)
            milestone.delete()
            return JsonResponse({'status': 'success'})
        except Milestone.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)

@login_required(login_url='/login/')
def update_milestone_api(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            milestone = Milestone.objects.get(pk=pk)
            milestone.title = data.get('title', milestone.title)
            milestone.category = data.get('category', milestone.category)
            milestone.description = data.get('description', milestone.description)
            milestone.status = data.get('status', milestone.status)
            milestone.save()
            return JsonResponse({'status': 'success'})
        except Milestone.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)

# --- ERROR HANDLING ---

def custom_404(request, exception):
    return render(request, 'tracker/404.html', status=404)