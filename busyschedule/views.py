from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import render

from .forms import ClassScheduleForm, AvailableBlockForm
from .models import ClassSchedule, AvailableBlock, DAYS


# 🔹 Función para unificar bloques disponibles que se solapen
def merge_available_blocks(day):
    blocks = AvailableBlock.objects.filter(day=day).order_by('start_time')

    merged = []
    for block in blocks:
        if not merged or merged[-1].end_time < block.start_time:
            merged.append(block)
        else:
            # Solapa → extendemos el último bloque
            merged[-1].end_time = max(merged[-1].end_time, block.end_time)
            merged[-1].save()
            block.delete()  # eliminamos el duplicado


# 🔹 Nueva portada (mockup principal)
def main_home(request):
    return render(request, 'main_home.html')


# 🔹 Vista de gestión de horarios (antes home)
def schedule_home(request):
    schedules = sorted(
        ClassSchedule.objects.all(),
        key=lambda s: (s.day_index(), s.start_time)
    )
    blocks = sorted(
        AvailableBlock.objects.all(),
        key=lambda b: (b.day_index(), b.start_time)
    )

    # Agrupamos bloques por día
    blocks_by_day = defaultdict(list)
    for b in blocks:
        blocks_by_day[b.day].append(b)

    if request.method == 'POST':
        if 'save_schedule' in request.POST:  # 🔹 se intenta agregar horario ocupado
            form_schedule = ClassScheduleForm(request.POST)
            form_block = AvailableBlockForm()
            if form_schedule.is_valid():
                new_schedule = form_schedule.save()

                # 🔹 Eliminar bloques disponibles que se solapen
                overlapping_blocks = AvailableBlock.objects.filter(
                    day=new_schedule.day,
                    start_time__lt=new_schedule.end_time,
                    end_time__gt=new_schedule.start_time
                )
                if overlapping_blocks.exists():
                    count = overlapping_blocks.count()
                    overlapping_blocks.delete()
                    messages.info(request, f"{count} bloque(s) de disponibilidad eliminado(s) por conflicto con '{new_schedule.subject}'.")

                return redirect('schedule_home')

        elif 'save_block' in request.POST:
            form_block = AvailableBlockForm(request.POST)
            form_schedule = ClassScheduleForm()
            if form_block.is_valid():
                new_block = form_block.save()
                merge_available_blocks(new_block.day)  # 🔹 Unificar bloques solapados
                return redirect('schedule_home')
    else:
        form_schedule = ClassScheduleForm()
        form_block = AvailableBlockForm()

    return render(request, 'home.html', {
        'schedules': schedules,
        'blocks_by_day': dict(blocks_by_day),
        'form_schedule': form_schedule,
        'form_block': form_block
    })


# 🔹 Modal de edición de horarios
def edit_schedule_modal(request, pk):
    schedule = get_object_or_404(ClassSchedule, pk=pk)
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            updated_schedule = form.save()

            # 🔹 Buscar bloques disponibles que se solapen con el horario editado
            overlapping_blocks = AvailableBlock.objects.filter(
                day=updated_schedule.day,
                start_time__lt=updated_schedule.end_time,
                end_time__gt=updated_schedule.start_time
            )
            deleted_count = overlapping_blocks.count()
            overlapping_blocks.delete()

            # 🔹 Enviar mensaje en la respuesta JSON si se eliminaron bloques
            if deleted_count > 0:
                return JsonResponse({
                    'success': True,
                    'message': f"{deleted_count} bloque(s) de disponibilidad eliminado(s) por conflicto con '{updated_schedule.subject}'."
                })
            return JsonResponse({'success': True})
        else:
            html_form = render_to_string('edit_form.html', {'form': form, 'schedule': schedule}, request=request)
            return JsonResponse({'success': False, 'html_form': html_form})
    else:
        form = ClassScheduleForm(instance=schedule)

    html_form = render_to_string('edit_form.html', {'form': form, 'schedule': schedule}, request=request)
    return JsonResponse({'html_form': html_form})


# 🔹 Eliminar horario
def delete_schedule(request, pk):
    schedule = get_object_or_404(ClassSchedule, pk=pk)
    if request.method == 'POST':
        schedule.delete()
        return redirect('schedule_home')
    return render(request, 'confirm_delete.html', {'schedule': schedule})


# 🔹 Eliminar bloque disponible
def delete_block(request, pk):
    block = get_object_or_404(AvailableBlock, pk=pk)
    if request.method == 'POST':
        block.delete()
        return redirect('schedule_home')
    return render(request, 'confirm_delete.html', {'block': block})


# 🔹 Rutina
def routine_view(request):
    schedules = ClassSchedule.objects.all()
    blocks = AvailableBlock.objects.all()

    # 🔹 Intervalos de 1 hora (8 a.m. - 11 p.m.)
    hours = list(range(8, 23))
    days = [d[0] for d in DAYS]  # ["Lunes", "Martes", ..., "Domingo"]

    # 🔹 Calcular rowspan en horas completas
    for s in schedules:
        s.rowspan = max(1, s.end_time.hour - s.start_time.hour)

    for b in blocks:
        b.rowspan = max(1, b.end_time.hour - b.start_time.hour)

    return render(request, 'routine.html', {
        'schedules': schedules,
        'blocks': blocks,
        'hours': hours,
        'days': days
    })

