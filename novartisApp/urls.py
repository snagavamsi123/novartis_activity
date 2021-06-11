from django.urls import path
from novartisApp import views

urlpatterns = [
    path('',views.home,name='home'),
    path('contacts',views.contact_book,name='contacts'),
    path('add',views.addcontact,name='add'),
    path('addmanual',views.addmanually,name='addmanual'),
    path('addexcel',views.add_excel_data,name='addexcel'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('edit/<int:id>',views.edit,name='edit'),

]