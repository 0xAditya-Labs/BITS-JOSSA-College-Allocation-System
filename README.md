JOSSA-Style Seat Allocation Portal

Live Demo: https://bits-jossa-college-allocation-syste.vercel.app/

A streamlined, JOSSA-style seat allocation system designed to efficiently manage student data, facilitate seat allocation based on preferences and rank, and ensure secure access to placement information. Originally built as a terminal-based application, it has been upgraded to a Flask web portal with OTP-secured student result access via Twilio SMS.

Academic Context

This system was conceptualized and developed by B.Tech 2nd Semester Computer Science and Engineering students: Aditya, Adarsh, Bhimansh, and Jithender. The project was executed under the supervision of Dr. Kusum Bharti at Dr. B.R. Ambedkar National Institute of Technology, Jalandhar.

Features

Admin Portal — Register students with personal details (name, roll number, rank, phone number) and up to four college preferences, and execute the seat allocation engine.

Student Portal & Security — OTP verification is implemented to ensure secure access to placement information. Students must authenticate their identity before viewing their allocated campus and branch.

Downloadable Results — Full placement list exported as a permanent text file (students_placement.txt).

Random Sorting Algorithm — Each allocation run picks one of five sorting algorithms at random:

Bubble Sort

Insertion Sort

Selection Sort

Merge Sort

Quick Sort

Twilio OTP Verification In Action

When a student inputs their rank, the system fetches their registered phone number, generates a 6-digit OTP, and dispatches it via the Twilio REST API.

College Codes

Code

Campus

Branch

1

Pilani

CSE

2

Goa

CSE

3

Pilani

ECE

4

Goa

ECE

Total seats: 8 (2 per college-branch combination)

Setup & Installation

1. Clone the repository

<<<<<<< HEAD
git clone <your-repo-url>
=======
```bash
git clone https://github.com/0xAditya-Labs/BITS-JOSSA-College-Allocation-System.git
>>>>>>> 61e91b53b47bc9d7b3f35abe58afb0cbba0a352b
cd "BITS Allocation Python"


2. Create a virtual environment

python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate


3. Install dependencies

pip install -r requirements.txt


4. Configure Twilio credentials

Copy the example env file and add your Twilio credentials. These credentials (account SID, auth token, and Twilio phone number) are required to authorize the Twilio Client.

cp .env.example .env


Edit .env with your values from the Twilio Console:

TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
FLASK_SECRET_KEY=some-random-secret-string


Important: .env is listed in .gitignore and will not be pushed to GitHub. Only .env.example (with placeholder values) is committed.

5. Run the application

python app.py


Open http://localhost:5000 in your browser.

Usage Flow

Admin Flow

Go to Admin Portal (/admin).

Input student credentials and preference choices, which are temporarily stored in a dictionary before file processing.

Click Run Seat Allocation. Seats are allocated based on student preferences and availability, ensuring fair distribution.

Download the results file from the admin page.

Student Flow

Go to Student Portal (/student).

Enter your rank and click Send OTP.

Check your registered phone for the SMS.

Enter the received OTP. If the OTP matches, access is granted to the report card.

View details including roll number, name, phone number, and allocated campus/branch.

Project Structure

<<<<<<< HEAD
├── app.py                          # Flask web server (main entry point)
=======
```
├── app.py                          # Flask web server 
>>>>>>> 61e91b53b47bc9d7b3f35abe58afb0cbba0a352b
├── allocation.py                   # Seat allocation logic
├── sorting.py                      # Sorting algorithms (random selection)
├── twilio_otp.py                   # OTP generation & Twilio SMS
├── choice_order_and_seat_allocation.py  # Original CLI script 
├── Twilio_OTP_send.py              # Original OTP module 
├── getresult.py                    # Original result viewer 
├── templates/
│   ├── index.html                  # Home page
│   ├── admin.html                  # Admin portal
│   └── student.html                # Student portal
├── static/
│   └── style.css                   # Frontend styles
│   ├── UI.jpg                      # Admin/Student Portal UI
│   └── OTP_screenshot.jpg          # Twilio SMS preview
├── students_placement.txt          # Generated results file
├── .env.example                    # Env template 
├── .env                            # Your local credentials (gitignored)
├── requirements.txt
└── README.md


API Endpoints

Method

Endpoint

Description

<<<<<<< HEAD
GET
=======
```bash
git init
git add .
git commit -m "Initial commit: BITS seat allocation portal"
git remote add origin https://github.com/0xAditya-Labs/BITS-JOSSA-College-Allocation-System.git
git push -u origin main
```
>>>>>>> 61e91b53b47bc9d7b3f35abe58afb0cbba0a352b

/

Home page

GET

/admin

Admin portal

GET

/student

Student portal

GET

/api/students

List registered students

POST

/api/students

Add a student

POST

/api/run-allocation

Run seat allocation

POST

/api/send-otp

Send OTP to student

POST

/api/verify-otp

Verify OTP & get result

GET

/api/download-results

Download placement txt file

GET

/api/status

System status

Future Scope

While the current implementation manages the core workflows of data entry, preference management, and allocation, future iterations of the project are planned to include:

Database Integration: Migrating from file-based storage to MySQL to add flexibility and advanced functionalities.

CRUD Operations: Adding the ability to delete, add, and update choice orders and database information within a given deadline.

Advanced Counseling: Incorporating multi-round systems and CSAB rounds for real-world scaling.

Data Validation: Implementing strict filters to avoid data ambiguity, such as duplicate roll numbers or ranks.

Direct SMS Reporting: Sending the final allocated college and branch directly via SMS on result day, alongside the OTP.

Enhanced Security: Adding a password generator to provide an additional layer of account protection.

License
MIT