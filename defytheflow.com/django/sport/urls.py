from django.urls import path, re_path

import sport

from .views import (show_all_workouts,
                    show_workout_detail,
                    add_new_workout,
                    update_workout_detail,
                    delete_workout,
                    show_all_time_stats,
                    show_this_week_stats,
                    show_this_month_stats,
                    suggest_workout,
                    )


urlpatterns = [

    path('', show_all_workouts, name='list'),
    path('stats/', show_all_time_stats, name='all-time-stats'),
    path('stats/this-week', show_this_week_stats, name='this-week-stats'),
    path('stats/this-month', show_this_month_stats, name='this-month-stats'),
    path('suggest/', suggest_workout, name='suggest'),
    path('add-new-workout/', add_new_workout, name='add-new-workout'),
    path('<str:workout_date>/', show_workout_detail, name='workout-detail'),
    path('<str:workout_date>/update/', update_workout_detail, name='update-workout-detail'),
    path('<str:workout_date>/delete/', delete_workout, name='delete-workout'),

]

handler404 = sport.views.handler404
handler500 = sport.views.handler500

