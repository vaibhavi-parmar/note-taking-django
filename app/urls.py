from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('sign-up/', views.SignUpView.as_view(), name='sign_up'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('list/', views.notes_list, name='list'),
    path('create/', views.create, name='create'),
    path('note/id=<int:id>/', views.detail, name='detail'),
    path('edit/id=<int:id>/', views.edit, name='edit'),
    path('delete/id=<int:id>/', views.delete, name='delete'),
    path('toggle_pin/id=<int:id>/', views.toggle_pin, name='toggle_pin'),
    path('archive/', views.archive, name='archive'),
    path('toggle_archive/id=<int:id>/', views.toggle_archive, name='toggle_archive'),
    path('bin/', views.bin, name='bin'),
    path('toggle_bin/id=<int:id>/', views.toggle_bin, name='toggle_bin'),
    path('share/<uuid:share_uuid>/', views.share, name='share'),
    path('export_pdf/<int:id>/', views.export_pdf, name='export_pdf'),
    path('export_txt/<int:id>/', views.export_txt, name='export_txt'),
]