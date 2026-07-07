import os
import random

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# In-memory OTP store: {rank: otp}
otp_store = {}


def generate_otp():
    """Generate a 6-digit OTP."""
    otp = 0
    for _ in range(6):
        otp = otp * 10 + random.randint(1, 9)
    return otp


def send_otp(phone_number, otp):
    """Send OTP via Twilio SMS."""
    if not all([ACCOUNT_SID, AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
        raise ValueError(
            "Twilio credentials missing. Set TWILIO_ACCOUNT_SID, "
            "TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER in your .env file."
        )

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body=f"Hello, your JOSSA OTP login is: {otp}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number,
    )
    return message.sid


def request_otp(rank, data):
    """Generate and send OTP to the student's registered phone number."""
    if rank not in data:
        raise KeyError(f"No student found with rank {rank}")

    phone_number = data[rank][2]
    if not phone_number.startswith("+"):
        phone_number = "+91" + phone_number

    otp = generate_otp()
    send_otp(phone_number, otp)
    otp_store[rank] = otp
    return otp


def verify_otp(rank, otp_given):
    """Verify OTP entered by the student."""
    stored = otp_store.get(rank)
    if stored is None:
        return False
    return int(stored) == int(otp_given)


def clear_otp(rank):
    """Remove OTP after successful verification."""
    otp_store.pop(rank, None)
