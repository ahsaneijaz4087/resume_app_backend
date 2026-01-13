from django.urls import path
from . import views

urlpatterns = [
    # Item APIs
    path('items/create/', views.create_item),
    path('items/', views.list_items),
    path('items/update/<int:item_id>/', views.update_item),
    path('items/delete/<int:item_id>/', views.delete_item),

    # Auth APIs
    path('signup/', views.signup),
    path('login/', views.login),
]
