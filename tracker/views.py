from django.shortcuts import render
from django.http import JsonResponse
from .models import Milestone
import json

def milestone_list_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Milestone.objects.create(
            title=data['title'],
            category=data.get('category', 'General'),
            description=data.get('description', '')
        )
        return JsonResponse({'status': 'success'})

    milestones = Milestone.objects.all().values('id', 'title', 'category', 'description', 'date_created')
    return JsonResponse(list(milestones), safe=False)

def home_page(request):
    return render(request, 'tracker/index.html')

# ADD THIS NEW FUNCTION BELOW:
def delete_milestone_api(request, pk):
    if request.method == 'POST':
        try:
            milestone = Milestone.objects.get(pk=pk)
            milestone.delete()
            return JsonResponse({'status': 'success'})
        except Milestone.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)