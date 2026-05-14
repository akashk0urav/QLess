from django.urls import path
from .views import create_venue_by_owner, get_unverified_venues, list_venues, create_venue, verify_venue
urlpatterns = [
    path('list/venues/', list_venues, name='list_venues'),
    path('create/venue/', create_venue, name='create_venue'),
    path('create/venue/owner/', create_venue_by_owner, name='create_venue_by_owner'),
    path('unverified/venues/', get_unverified_venues, name='get_unverified_venues'),
    path('verify/venue/<int:venue_id>/', verify_venue, name='verify_venue'),
]
