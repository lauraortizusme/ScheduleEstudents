from django.shortcuts import render, redirect
from .forms import ClassScheduleForm
from .models import ClassSchedule
from django.shortcuts import get_object_or_404
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

def edit_schedule(request, pk):
    schedule = get_object_or_404(ClassSchedule, pk=pk)
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClassScheduleForm(instance=schedule)
    return render(request, 'schedule.html', {'form': form})

def delete_schedule(request, pk):
    schedule = get_object_or_404(ClassSchedule, pk=pk)
    if request.method == 'POST':
        schedule.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'schedule': schedule})
