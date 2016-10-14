from django.conf.urls import include, url
from . import views


urlpatterns = (
    url(r'^mygoals$', views.mygoals_page, name='my_goals'),
    url(r'^mygoals/savings$', views.savings_goals_page, name='savings_goals'),
    url(r'^mygoals/credit$', views.credit_goals_page, name='credit_goals'),
    url(r'^mygoals/final$', views.final_goal_page, name='final_goals'),
    url(r'^mygoals/(\d+)/(\d+)/complete$', views.goal_complete_page, name='goal_completed'),
    url(r'^mygoals/(\d+)/(\d+)/sorry$', views.goal_failed_page, name='goal_failed'),

)
