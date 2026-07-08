from Twilio_OTP_send import *

# Maximum seats : 8(2x2x2)
# College Codes:-
# Pilani CSE : 1
# Goa CSE: 2
# Pilani ECE : 3
# Goa ECE: 4

def take_space(str,n):
    space=" "*(n-len(str))
    return str+space

    



data={}
#                           -------------FUNCTION FOR DATA ENTRY------------

def add_data(name,roll_no,rank,phone_number):
    choice=[]               # list having order of seat-code
    print("Enter 0 if want to exit : ")
    print("Enter your choice in order :-")
    i=1
    cnt=1
    while True:
        if(cnt>4):              
            break                          # becz there are only 4 colg_branch code
        ch=int(input(f"({i}) -> "))
        choice.append(ch)
        if ch==0:
            break
        i+=1
        cnt+=1
    d={rank:(roll_no,name,phone_number,choice)}     # Format of any index of data
    # global data       NO need becz data contains disctionaruy as object and is mutable.... Therefore global isnt needed at all
    data.update(d)

#                 ----------------Entering students inside data--------------------

applicants_count=int(input("Enter number of students appeared : "))
print()
for i in range(applicants_count):

    name=input("Enter your name : ")
    roll_no=int(input("Enter your Roll Number : "))
    rank=int(input("Enter your rank : "))
    phone=input("Enter phone number to be registered (OTP will come at this number) :  ")
    add_data(name,roll_no,rank,phone)
    print()


#------------------------------------FOR DATA CHNGES BY USER-------------------------------------------------

    # YET TO BE UPADTED------------------------------------------------------------ YET TO BE UPDATED



#------------------------------------FOR DATA PROCESSING----------------------------------------------------   
#                           (when JOSSA closes change portal for colleges)


ranks_registered=list(data.keys())
ranks_registered.sort()

# ranks_register are in sorted form and are keys for data


seats_available=[0,2,2,2,2]   # 0 at 0th index becz 0 is not any colg-branch code
#                               index representing the seat code

seat_alloated={}
counter=0    # records how many students get seat ; If it reaches 8 then break simce mno more seats available
for rank in ranks_registered:
    if counter>8:
        break
    got_seat=False
    pref_list=data[rank][3]
    for i in pref_list:             # i is current preference code
        if seats_available[i]>0:
            # cong aapko seat mil gya
            got_seat=True
            seat_alloated[rank]=i
            seats_available[i]-=1
            break
    if got_seat==True:
        counter+=1




#---------------------------------Appending Data inside a txt file-----------------------------------------


colg_list=[(0,0),   ('Pilani','CSE'),('Goa','CSE'),('Pilani','ECE'),('Goa','ECE')]    # Index represent colg code and branch

# Appending data of students inside the file
with open('students_placement.txt','a') as f:
    for rank in ranks_registered:
        f.write(take_space(str(rank),8))
        f.write(take_space(str(data[rank][0]),15))
        f.write(take_space(str(data[rank][1]),20))
        f.write(take_space(str(data[rank][2]),15))
        # seat_allocated[rank] gives me colg. code for the student(rank) if effectrive_rank<8
        # colg_list has info of colg and branch as colg_code=index of this list if effectrive_rank<8

        # Assuming all ranks are continous
        if(rank<8):                         # Actually it must be ranks_registered[8] in place of 8
            colg_code=seat_alloated[rank]
            f.write(take_space(colg_list[colg_code][0],12))
            f.write(colg_list[colg_code][1])
        else:
            f.write("NOT QUALIFIED")
        f.write("\n")


# ---------------------------------------- Having Report Card -----------------------------------

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
        credentials=data[r]
        print(f'Roll Number : {credentials[0]}')
        print('Name :',credentials[1])
        print('Phone Number :',credentials[2])
        print()
        if rank<=8:
            colg_code=seat_alloated[rank]
            print('Campus Alloated : IIIT',colg_list[colg_code][0])
            print('Branch :',colg_list[colg_code][1])
        else:
            print("Not Qualified\nAll The Best for Next Time")
    else:
        print("WRONG OTP !!!")
    print()
    print()
