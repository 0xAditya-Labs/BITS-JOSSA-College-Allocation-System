print("\t\t\t*** REPORT CARD ***\n\n\n")")

print("Enter 0 in rank if you want to stop \n\n")
while True:
    r=int(input("Enter your rank : "))
    if r==0:
        print("Thankyou !!!")
        break

    # ------FOR SECURITY CHECKS-----
    recieved_otp=OTP(r,data)
    otp_given_by_user=int(input("Enter recieved OTP : "))
    print()

    if recieved_otp==otp_given_by_user:
        