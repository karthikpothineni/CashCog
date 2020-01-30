from django.conf.urls import url, include
from .views.expenseViews import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'v1/expense', ExpenseViewSet ,base_name='expenses')


urlpatterns = [
    url(r'^v1/sort', ExpenseViewSet.as_view({'get': 'sort_expenses'}), name='sort_expenses'),
    url(r'^v1/health',  healthcheck_view.as_view()),
    url(r'^', include(router.urls)),
]
