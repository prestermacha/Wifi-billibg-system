
from django.urls import path
from .views import StoreConfigView,StoreListView,StoreUpdateView,DeleteStore,StoreDetailsView,WarehouseListView,AddWarehouseView,WarehouseDetailsView,WarehouseUpdate,DeleteWarehouse,RegisterListView,AddRegisterView,RegisterDetailsView,RegisterUpdate,DeleteRegister

urlpatterns=[
    # warehouse
    path('warehouse/',WarehouseListView.as_view(),name='warehouse-list'),
    path('warehouse/add/',AddWarehouseView.as_view(),name='add-warehouse'),
    path('warehouse/<str:warehouse_id>/',WarehouseDetailsView.as_view(),name='warehouse-details'),
    path('warehouse/<str:warehouse_id>/update/',WarehouseUpdate.as_view(),name='update-warehouse'),
    path('warehouse/<str:warehouse_id>/delete/',DeleteWarehouse.as_view(), name='delete-warehouse'),

    # register
    path('register/',RegisterListView.as_view(),name='register-list'),
    path('register/add/',AddRegisterView.as_view(),name='add-register'),
    path('register/<str:register_id>/',RegisterDetailsView.as_view(),name='register-details'),
    path('register/<str:register_id>/update/',RegisterUpdate.as_view(),name='update-register'),
    path('register/<str:register_id>/delete/',DeleteRegister.as_view(), name='delete-register'),

    
    # store
    path('add/',StoreConfigView.as_view(),name='add-store'),  
    path('store-list/',StoreListView.as_view(),name='store-list'),  
    path('<str:store_id>/',StoreDetailsView.as_view(),name='store-details'), 
    path('<str:store_id>/update/',StoreUpdateView.as_view(),name='update-store'),
    path('<str:store_id>/delete/',DeleteStore.as_view(), name='store-delete'),


]