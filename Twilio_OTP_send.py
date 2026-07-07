"""
Legacy OTP module — now uses environment variables via twilio_otp.py.
Import from twilio_otp for new code.
"""

from twilio_otp import generate_otp, request_otp, send_otp, verify_otp


def OTP(rank, data):
    """Backward-compatible wrapper for request_otp."""
    return request_otp(rank, data)
