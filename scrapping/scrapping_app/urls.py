from django.urls import path
from .views import GetAuctions,GetAuctionsSuperrare

urlpatterns = [
    path('auctions_foundation', GetAuctions.as_view()),
    path('auctions_superrare', GetAuctionsSuperrare.as_view())
]