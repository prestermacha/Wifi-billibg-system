
from django.urls import path
from .views import BranchConfigView,BranchDetailsView,DeleteBranch,BranchUpdateView,BranchListView
urlpatterns=[

    
    # store
    path('add/',BranchConfigView.as_view(),name='add-branch'),  
    path('branch-list/',BranchListView.as_view(),name='branch-list'),  
    path('<str:branch_id>/',BranchDetailsView.as_view(),name='branch-details'), 
    path('<str:branch_id>/update/',BranchUpdateView.as_view(),name='update-branch'),
    path('<str:branch_id>/delete/',DeleteBranch.as_view(), name='branch-delete'),


]