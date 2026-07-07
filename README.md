# BITS Seat Allocation Portal

A JOSSA-style seat allocation system for BITS campuses with OTP-secured student result access via Twilio SMS.

## Features

- **Admin Portal** — Register students with college preferences and run seat allocation
- **Student Portal** — OTP verification via Twilio to view individual report cards
- **Downloadable Results** — Full placement list exported as `students_placement.txt`
- **Random Sorting Algorithm** — Each allocation run picks one of five sorting algorithms at random:
  - Bubble Sort
  - Insertion Sort
  - Selection Sort
  - Merge Sort
  - Quick Sort

## College Codes

| Code | Campus | Branch |
|------|--------|--------|
| 1    | Pilani | CSE    |
| 2    | Goa    | CSE    |
| 3    | Pilani | ECE    |
| 4    | Goa    | ECE    |

Total seats: **8** (2 per college-branch combination)

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd "BITS Allocation Python"
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Twilio credentials

Copy the example env file and add your Twilio credentials:

```bash
cp .env.example .env
```

Edit `.env` with your values from the [Twilio Console](https://console.twilio.com/):

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
FLASK_SECRET_KEY=some-random-secret-string
```

> **Important:** `.env` is listed in `.gitignore` and will **not** be pushed to GitHub. Only `.env.example` (with placeholder values) is committed.

### 5. Run the application

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## Usage

### Admin Flow

1. Go to **Admin Portal** (`/admin`)
2. Add students with name, roll number, rank, phone, and college preferences
3. Click **Run Seat Allocation** when all students are registered
4. Download the results file from the admin page or student portal

### Student Flow

1. Go to **Student Portal** (`/student`)
2. Enter your rank and click **Send OTP**
3. Check your registered phone for the SMS
4. Enter the OTP and view your report card
5. Optionally download the full `students_placement.txt` file

## Project Structure

```
├── app.py                          # Flask web server (main entry point)
├── allocation.py                   # Seat allocation logic
├── sorting.py                      # Sorting algorithms (random selection)
├── twilio_otp.py                   # OTP generation & Twilio SMS
├── choice_order_and_seat_allocation.py  # Original CLI script (legacy)
├── Twilio_OTP_send.py              # Original OTP module (legacy)
├── getresult.py                    # Original result viewer (legacy)
├── templates/
│   ├── index.html                  # Home page
│   ├── admin.html                  # Admin portal
│   └── student.html                # Student portal
├── static/
│   └── style.css                   # Frontend styles
├── students_placement.txt          # Generated results file
├── .env.example                    # Env template (safe for GitHub)
├── .env                            # Your local credentials (gitignored)
├── requirements.txt
└── README.md
```

## API Endpoints

| Method | Endpoint              | Description                    |
|--------|-----------------------|--------------------------------|
| GET    | `/`                   | Home page                      |
| GET    | `/admin`              | Admin portal                   |
| GET    | `/student`            | Student portal                 |
| GET    | `/api/students`       | List registered students       |
| POST   | `/api/students`       | Add a student                  |
| POST   | `/api/run-allocation` | Run seat allocation            |
| POST   | `/api/send-otp`       | Send OTP to student            |
| POST   | `/api/verify-otp`     | Verify OTP & get result        |
| GET    | `/api/download-results` | Download placement txt file  |
| GET    | `/api/status`         | System status                  |

## Pushing to GitHub

The repo is safe to push as-is:

- `.env` is gitignored (your real credentials stay local)
- `.env.example` has placeholder values for other developers
- No secrets are hardcoded in the source code

```bash
git init
git add .
git commit -m "Initial commit: BITS seat allocation portal"
git remote add origin <your-repo-url>
git push -u origin main
```

## Legacy CLI Scripts

The original command-line scripts are still available:

- `choice_order_and_seat_allocation.py` — Interactive CLI for data entry and allocation
- `Twilio_OTP_send.py` — Standalone OTP module
- `getresult.py` — Standalone result viewer

The web app (`app.py`) is the recommended way to run the system.

## Future Scope

See `future_scope.txt` for planned enhancements (multi-round counselling, data CRUD, duplicate validation, etc.).

## License

MIT
