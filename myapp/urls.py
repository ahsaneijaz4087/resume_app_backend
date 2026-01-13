from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.list_items, name='list_items'),                    # GET all
    path('items/create/', views.create_item, name='create_item'),           # POST
    path('items/<int:item_id>/', views.get_item, name='get_item'),           # GET single
    path('items/<int:item_id>/update/', views.update_item, name='update_item'),  # PUT/PATCH
    path('items/<int:item_id>/delete/', views.delete_item, name='delete_item'),  # DELETE
]