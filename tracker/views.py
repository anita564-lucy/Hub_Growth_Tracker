from django.shortcuts import render
from django.http import JsonResponse
from .models import Milestone
import json  # Make sure this is here!

# Update this function starting around line 6:
def milestone_list_api(request):
    if request.method == 'POST':
        # This part handles SAVING the new milestone
        data = json.loads(request.body)
        Milestone.objects.create(
            title=data['title'],
            category=data.get('category', 'General'),
            description=data.get('description', '')
        )
        return JsonResponse({'status': 'success'})

    # This part (the GET logic) handles SHOWING the milestones
    milestones = Milestone.objects.all().values('title', 'category', 'description', 'date_created')
    return JsonResponse(list(milestones), safe=False)

def home_page(request):
    return render(request, 'tracker/index.html')