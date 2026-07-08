from twilio.rest import Client
import random

# Twilio credentials
account_sid = 'abcd'
auth_token = 'abcd'
twilio_phone_number = '+1234'

# Function to generate OTP
def generate_otp():
    otp=0
    for i in range(6):                  # becz 6 digit OTP
        otp=otp*10+random.randint(1,9)
    return otp

# Function to send OTP via Twilio
def send_otp(phone_number, otp):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Hello, your JOSSA OTP login is: {otp}",
        from_=twilio_phone_number,
        to=phone_number
    )
    return message.sid

# Main function
def OTP(rank,data):
    phone_number=data[rank][2]
    # Get user input for phone number
    # phone_number = input("Enter your phone number to send OTP: ")
    phone_number='+91'+phone_number

    # Generate OTP
    otp = generate_otp()

    # Send OTP
    message_sid = send_otp(phone_number, otp)
    print(f"OTP sent successfully to {phone_number}!")
    return otp

# We have registered phone number of student
# On enetering roll number , we can map his phone number and send OTP to that number 
# if student manged to give OTP then he can access the report card of candidate

#                            AFTER SOME TIME OF FULFILMENT OF THIS PROJECT
 
# if our website is prepared then this process is done to login 
# our site for that particular student













# otp=OTP()
# otp_recieved=int(input("Enter the OTP : "))
# if otp==otp_recieved:
#     print("You are registered")


