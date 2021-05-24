from django.urls import path
from .views import GetAuctions,GetAuctionsSuperrare,GetAuctionsRarible,GetAuctionsMakersplace,GetAuctionsOpensea

urlpatterns = [
    path('auctions_foundation', GetAuctions.as_view()),
    path('auctions_superrare', GetAuctionsSuperrare.as_view()),
    path('auctions_rarible', GetAuctionsRarible.as_view()),
    path('auctions_makersplace', GetAuctionsMakersplace.as_view()),
    path('auctions_opensea', GetAuctionsOpensea.as_view())
]