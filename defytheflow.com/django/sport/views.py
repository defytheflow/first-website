from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from datetime import datetime
import csv

from .models import Workout
from .forms import WorkoutModelForm


# list
@login_required
def show_all_workouts(request):
    workouts = Workout.objects.order_by('-date')
    template_name = 'sport/list.html'
    context = {'workouts': workouts}
    return render(request, template_name, context)

# detail
@login_required
def show_workout_detail(request, workout_date):
    workout = get_object_or_404(Workout, date=workout_date)
    template_name = 'sport/detail.html'
    context = {'workout': workout}
    return render(request, template_name, context)

# create
@login_required
@staff_member_required
def add_new_workout(request):
    if request.method == 'POST':
        form = WorkoutModelForm(request.POST)
        if form.is_valid():
            new_workout = form.save(commit=False)
            new_workout.user = request.user
            new_workout.body_part1 = new_workout.body_part1.capitalize()
            if new_workout.body_part2:
                new_workout.body_part2 = new_workout.body_part2.capitalize()
            if new_workout.cardio:
                new_workout.cardio = new_workout.cardio.capitalize()
            if new_workout.cardio_load:
                new_workout.cardio_load = new_workout.cardio_load.capitalize()
            new_workout.summary = new_workout.summary.capitalize()
            save_data_to_csv('add', new_workout)
            new_workout.save()
            return HttpResponseRedirect('/sport/')
        else:
            return HttpResponseRedirect('/sport/500.html')
    else:
        form = WorkoutModelForm()
    template_name = 'sport/add-form.html'
    context = {'form': form, 'today': str(datetime.now().date())}
    return render(request, template_name, context)

# update
@login_required
@staff_member_required
def update_workout_detail(request, workout_date):
    workout = get_object_or_404(Workout, date=workout_date)
    form = WorkoutModelForm(request.POST or None, instance=workout)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            save_data_to_csv('update')
            return HttpResponseRedirect(f'/sport/{workout_date}')
        else:
            return HttpResponseRedirect('/sport/500.html')
    template_name = 'sport/update-form.html'
    context = {'form': form, 'workout_date': workout_date, 'workout': workout}
    return render(request, template_name, context)

# delete
@login_required
@staff_member_required
def delete_workout(request, workout_date):
    workout = get_object_or_404(Workout, date=workout_date)
    if request.method == 'POST':
        workout.delete()
        return HttpResponseRedirect('/sport/')
    template_name = 'sport/delete.html'
    context = {'workout': workout}
    return render(request, template_name, context)


def handler404(request, exception):
    return render(request, 'sport/404.html', status=404)


def handler500(request):
    return render(request, 'sport/500.html', status=500)


# STATS
def show_all_time_stats(request):
    workouts = Workout.objects.all()
    b = [workout.body_part1 for workout in workouts] + \
        [workout.body_part2 for workout in workouts if workout.body_part2 is not None]
    dct = {}
    for item in b:
        if item not in dct.keys():
            dct[item] = 1
        else:
            dct[item] += 1
    body_parts = list(dct.keys())
    count = list(dct.values())
    template_name = 'sport/stats.html'
    context = {'labels': body_parts, 'data': count, 'dct': dct}
    return render(request, template_name, context)


def show_this_week_stats(request):
    month = datetime.now().month
    workouts = Workout.objects.filter(date__month=month)
    dates = [workout.date for workout in workouts]
    weekdays = [date.weekday() for date in dates]
    dct = {}
    for i in range(len(dates)):
        dct[weekdays[i]] = dates[i]
    a = weekdays.index(0)
    this_week = weekdays[a:]
    this_week_dates = [dct[weekday] for weekday in this_week]
    body_parts = [workout.body_part1 for workout in workouts if workout.date in this_week_dates] + \
                 [workout.body_part2 for workout in workouts if workout.date in this_week_dates and workout.body_part2 is not None]
    count = [body_parts.count(body_part) for body_part in set(body_parts)]
    template_name = 'sport/this_week_stats.html'
    context = {'labels': set(body_parts), 'data': count}
    return render(request, template_name, context)


def show_this_month_stats(request):
    workouts = Workout.objects.filter(date__month='6')
    body_parts = [workout.body_part1 for workout in workouts] + \
                 [workout.body_part2 for workout in workouts if workout.body_part2 is not None]
    dct = {}
    for item in body_parts:
        if item not in dct.keys():
            dct[item] = 1
        else:
            dct[item] += 1
    body_parts = list(dct.keys())
    count = list(dct.values())
    template_name = 'sport/this_month_stats.html'
    context = {'labels': body_parts, 'data': count, 'dct': dct}
    return render(request, template_name, context)


def suggest_workout(request):
    body_parts = {'Chest', 'Arms', 'Shoulders', 'Back'}
    workouts = Workout.objects.order_by('-date')
    b = [workout.body_part1 for workout in workouts]
    last_4_workouts = set(b[:4])

    if body_parts.difference(last_4_workouts) == set():
        suggestion = [b[:4][-1]]
    elif len(body_parts.difference(last_4_workouts)) >= 1:
        suggestion = list(body_parts.difference(last_4_workouts))

    template_name = 'sport/suggest.html'
    context = {'suggestion': suggestion}
    return render(request, template_name, context)


def save_data_to_csv(mode, workout: Workout = None):
    columns = ['date', 'body_part1', 'num_exercises1', 'body_part2',
               'num_exercises2', 'cardio', 'cardio_load', 'summary']
    if mode == 'update':
        workouts = Workout.objects.all()
        data = [columns]
        file = open('sport/csv/sport/data.csv', 'w')
        with file:
            writer = csv.writer(file)
            writer.writerows(data)

        for workout in workouts:
            workout = [workout.date, workout.body_part1, workout.num_exercises1,
                       workout.body_part2, workout.num_exercises2,
                       workout.cardio, workout.cardio_load, workout.summary]
            data = [workout]
            file = open('sport/csv/sport/data.csv', 'a')
            with file:
                writer = csv.writer(file)
                writer.writerows(data)
    elif mode == 'add':
        workout = [workout.date, workout.body_part1, workout.num_exercises1,
                   workout.body_part2, workout.num_exercises2,
                   workout.cardio, workout.cardio_load, workout.summary]
        data =[workout]
        file = open('sport/csv/sport/data.csv', 'a')
        with file:
            writer = csv.writer(file)
            writer.writerows(data)














