from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('members/', views.view_members, name='view_members'),
    path('addmember/', views.add_members, name='addmember'),
    path('books/', views.view_books, name='view_book'),
    path('borrow/', views.borrow, name='borrow'),
    path('addbook/', views.addbooks, name='addbook'),
    path('returnbook/',views.returnbook,name='returnbook'),
    path('updatebook/', views.updatebook, name='update_book'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
]
