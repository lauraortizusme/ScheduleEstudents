from django.shortcuts import render, redirect
from .forms import ClassScheduleForm
from .models import ClassSchedule
# Create your views here.

def home(request):
    schedules = ClassSchedule.objects.all().order_by('day', 'start_time')
    return render(request, 'home.html', {'schedules': schedules})

def add_schedule(request):
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClassScheduleForm()
    return render(request, 'schedule.html', {'form': form})