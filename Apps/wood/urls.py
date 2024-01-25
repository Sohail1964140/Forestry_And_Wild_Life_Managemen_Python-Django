from django.urls import path
from . import views

app_name="wood"

urlpatterns = [
    
    path('entry/', views.woodAddView.as_view(), name="woodEntryAdd"),
    path('list/', views.woodListView.as_view(), name="woodEntryList"),
    path('update/<int:id>', views.woodUpdateView.as_view(), name="woodEntryUpdate"),
    path('delete/<int:id>', views.woodDeleteView.as_view(), name="woodEntryDelete"),
    path('search/>', views.woodSearchView.as_view(), name="woodEntrySearch"),
    
    # Auction paths
    path('auction/search/>', views.auctionSearchView.as_view(), name="auctionSearch"),
    path("auction/add/", views.auctionAddView.as_view(), name="auctionAdd"),
    path("auction/list/", views.auctionListView.as_view(), name="auctionList"),
    path('auction/update/<int:id>/', views.auctionUpdateView.as_view(), name="auctionUpdate"),
    path('auction/delete/<int:id>/', views.auctionDeleteView.as_view(), name="auctionDelete"),
    
    
    
     # Tree Alatment paths
    path('tree-alatment/search/>', views.treeAlatmentSearchView.as_view(), name="alatmentSearch"),
    path("tree-alatment/add/", views.treeAlatmentAddView.as_view(), name="alatmentAdd"),
    path("tree-alatment/list/", views.treeAlatmentListView.as_view(), name="alatmentList"),
    path('tree-alatment/update/<int:id>/', views.treeAlatmentUpdateView.as_view(), name="alatmentUpdate"),
    path('tree-alatment/delete/<int:id>/', views.treeAlatmentDeleteView.as_view(), name="alatmentDelete"),
]
