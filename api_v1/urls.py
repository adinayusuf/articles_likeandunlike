from django.urls import path

from api_v1.views import add, subtract, multiply, divide

app_name = 'api_v1'

urlpatterns = [
    path('add/', add),
    path('subtract/', subtract),
    path('multiply/', multiply),
    path('divide/', divide),
]
