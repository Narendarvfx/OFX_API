from django.shortcuts import render

# Create your views here.

def shotAssignmentsUI(request):
    return render(request, 'shotassignments/shotassignments.html')