import random
from django.core.cache import cache

OTP_EXPIRATION_TIME = 300  # OTP expiration time in seconds (5 minutes)

def generate_otp():
    return str(
        random.randint(100000, 999999)  # Generate a random 6-digit OTP
    )

def store_otp(phone, otp):
    key=f"otp:{phone}"
    cache.set(
        key, otp, OTP_EXPIRATION_TIME
    ) # Store OTP with expiration time

def get_stored_otp(phone):
    key=f"otp:{phone}"
    return cache.get(key)  # Retrieve OTP from Redis

def delete_stored_otp(phone):
    key=f"otp:{phone}"
    cache.delete(key)  # Delete OTP from Redis



# How Redis stores it
# key: otp:+919812345678
# value: 4832
# ttl: 300 sec