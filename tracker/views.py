from django.shortcuts import render
from django.http import JsonResponse
from .models import Milestone

# This handles the data (The API)
def milestone_list_api(request):
    milestones = Milestone.objects.all().values('title', 'category', 'description', 'date_created')
    return JsonResponse(list(milestones), safe=False)

# This handles the webpage (The HTML)
# YOU ARE LIKELY MISSING THIS PART BELOW:
def home_page(request):
    return render(request, 'tracker/index.html')