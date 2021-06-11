from django.urls import path
from charts import views

urlpatterns = [
    path('',views.input,name='input'),
    path('output',views.output,name='output'),
    path('excelcharts',views.excel_output,name='excel_output')
]