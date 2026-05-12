from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, UserType
from .serializers import CustomerOTPSerializer, CustomerVerifyOTPSerializer, LoginSerializer, SignUpSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .otp_service import generate_otp, store_otp,delete_stored_otp,get_stored_otp

# Create your views here.

# generate token for user
def generate_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

# cutomomer otp request
@api_view(['POST'])
def customer_otp_request(request):
    serializer = CustomerOTPSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    phone = serializer.validated_data['phone']
    # hardcoded otp for testing
    otp=generate_otp()
    store_otp(phone, otp)
    print(f"OTP for {phone} is {otp}")  # In real application, send OTP via SMS gateway
    return Response(
        {
            "message":"OTP sent to phone number",
            "otp": otp
        }
    )

# customer otp verify
@api_view(['POST'])
def customer_otp_verify(request):
    serializer = CustomerVerifyOTPSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    phone = serializer.validated_data['phone']
    otp = serializer.validated_data['otp']
    stored_otp = get_stored_otp(phone)

    # hardcoded otp for testing
    if otp != stored_otp:
        return Response(
            {
                "error": "Invalid OTP"
            }, status=401
        )
    delete_stored_otp(phone)  # OTP is valid, delete it from Redis
    
    # get or create user based on phone number its try to find user with phone number 
    # if not found then create new user with phone number and default user type as customer
    user, created = User.objects.get_or_create(
        phone=phone,
        defaults={
            "username": phone,  # using phone number as username
            "user_type": UserType.CUSTOMER,
            "is_active": True
        }
    )
    token = generate_token(user)
    return Response(
        {
            "message": "OTP verified successfully",
            "token": token,
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "phone": user.phone,
                "user_type": user.user_type,
            }
        }
    )

# staff login with email and password
@api_view(['POST'])
def staff_login(request):
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    user = authenticate(username=email, password=password)
    if not user or user.user_type != UserType.STAFF:
        return Response(
            {
                "error": "Invalid credentials or user is not staff"
            }, status=401
        )
    token = generate_token(user)
    return Response(
        {
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "user_type": user.user_type,
            }
        }
    )

# owner login with email and password
@api_view(['POST'])
def owner_login(request):
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    user = authenticate(username=email, password=password)
    if not user or user.user_type != UserType.OWNER:
        return Response(
            {
                "error": "Invalid credentials or user is not owner"
            }, status=401
        )
    token = generate_token(user)
    return Response(
        {
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "user_type": user.user_type,
            }
        }
    )

# owner or staff sign up 
@api_view(['POST'])
def owner_staff_signup(request):
    serializer = SignUpSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    full_name = serializer.validated_data['full_name']
    email = serializer.validated_data['email']
    phone = serializer.validated_data['phone']
    password = serializer.validated_data['password']        
    user_type = serializer.validated_data['user_type']
    gender = serializer.validated_data['gender']
    if user_type not in [UserType.OWNER, UserType.STAFF]:
        return Response(
            {
                "error": "Invalid user type for this endpoint"
            }, status=400
        )
    if User.objects.filter(email=email).exists():
        return Response(
            {
                "error": "Email already exists"
            }, status=400
        )
    if User.objects.filter(phone=phone).exists():
        return Response(
            {
                "error": "Phone number already exists"
            }, status=400
        )
    # create_user method will handle password hashing and user creation
    user = User.objects.create_user(
        username=email,
        full_name=full_name,
        email=email,
        phone=phone,
        password=password,
        user_type=user_type,
        gender=gender,
        is_active=True
    )
    token = generate_token(user)
    return Response(
        {
            "message": "User created successfully",
            "token": token,
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "user_type": user.user_type,
                "gender": user.gender,
            }
        }
    )