from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Venue, VenueMember
from .serializers import VenueSerializer

from .permissions import IsAdmin, IsOwner
from rest_framework.permissions import IsAuthenticated

# this view is open to all users, but only returns verified venues
# unverified venues can only be seen by admins and the owners who created them
@api_view(['GET'])
def list_venues(request):
    venues = Venue.objects.filter(is_venue_verified=True)
    serializer = VenueSerializer(venues, many=True)
    return Response(serializer.data)

# creating venues by admins and this is allready verified
@api_view(['POST'])
@permission_classes([IsAuthenticated & IsAdmin])
def create_venue(request):
    serializer = VenueSerializer(data=request.data)
    if serializer.is_valid():
        venue = serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# venue is created by owner and this is not verified until admin verify it
@api_view(['POST'])
@permission_classes([IsAuthenticated & IsOwner])
def create_venue_by_owner(request):
    serializer = VenueSerializer(data=request.data)
    if serializer.is_valid():
        venue = serializer.save()
        # Add the creator as the owner of the venue
        VenueMember.objects.create(
            venue=venue,
            user=request.user,
            role=VenueMember.Role.OWNER
        )
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# admin can see all unverified venues and verify them
@api_view(['GET'])
@permission_classes([IsAuthenticated & IsAdmin])
def get_unverified_venues(request):
    venues = Venue.objects.filter(is_venue_verified=False)
    serializer = VenueSerializer(venues, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated & IsAdmin])
def verify_venue(request, venue_id):
    try:
        venue = Venue.objects.get(id=venue_id)
        venue.is_venue_verified = True
        venue.save()
        return Response({"message": "Venue verified successfully."}, status=200)
    except Venue.DoesNotExist:
        return Response({"error": "Venue not found."}, status=404)
    


# Create your views here.
