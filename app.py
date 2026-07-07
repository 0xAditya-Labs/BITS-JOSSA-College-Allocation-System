import os

from flask import Flask, jsonify, render_template, request, send_file

from allocation import (
    add_student,
    allocate_seats,
    generate_placement_file,
    get_student_result,
)
from twilio_otp import clear_otp, request_otp, verify_otp

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "bits-allocation-dev-key")

# Application state
students_data = {}
seat_allocated = {}
sorted_ranks = []
sorting_algorithm_used = None
allocation_done = False
placement_file = "students_placement.txt"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin")
def admin():
    return render_template(
        "admin.html",
        students=students_data,
        allocation_done=allocation_done,
        sorting_algorithm=sorting_algorithm_used,
    )


@app.route("/student")
def student():
    return render_template("student.html", allocation_done=allocation_done)


@app.route("/api/students", methods=["GET"])
def list_students():
    students = []
    for rank, (roll_no, name, phone, choices) in students_data.items():
        students.append(
            {
                "rank": rank,
                "roll_no": roll_no,
                "name": name,
                "phone": phone,
                "choices": choices,
            }
        )
    return jsonify({"students": students, "count": len(students)})


@app.route("/api/students", methods=["POST"])
def create_student():
    payload = request.get_json() or {}
    try:
        rank = int(payload["rank"])
        roll_no = int(payload["roll_no"])
        name = str(payload["name"]).strip()
        phone = str(payload["phone"]).strip()
        choices = [int(c) for c in payload.get("choices", [])]
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid student data. Check all fields."}), 400

    if allocation_done:
        return jsonify({"error": "Allocation already completed. Cannot add more students."}), 400

    try:
        add_student(students_data, name, roll_no, rank, phone, choices)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"message": "Student added successfully.", "rank": rank}), 201


@app.route("/api/run-allocation", methods=["POST"])
def run_allocation():
    global seat_allocated, sorted_ranks, sorting_algorithm_used, allocation_done

    if not students_data:
        return jsonify({"error": "No students registered. Add students first."}), 400

    if allocation_done:
        return jsonify({"error": "Allocation has already been run."}), 400

    sorted_ranks, seat_allocated, sorting_algorithm_used = allocate_seats(students_data)
    generate_placement_file(students_data, sorted_ranks, seat_allocated, placement_file)
    allocation_done = True

    return jsonify(
        {
            "message": "Seat allocation completed.",
            "sorting_algorithm": sorting_algorithm_used,
            "students_allocated": len(seat_allocated),
            "total_students": len(students_data),
        }
    )


@app.route("/api/send-otp", methods=["POST"])
def send_otp_route():
    if not allocation_done:
        return jsonify({"error": "Results are not published yet."}), 400

    payload = request.get_json() or {}
    try:
        rank = int(payload["rank"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Valid rank is required."}), 400

    if rank not in students_data:
        return jsonify({"error": f"No student found with rank {rank}."}), 404

    try:
        request_otp(rank, students_data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 500
    except Exception as exc:
        return jsonify({"error": f"Failed to send OTP: {exc}"}), 500

    phone = students_data[rank][2]
    masked = phone[:2] + "****" + phone[-2:] if len(phone) > 4 else "****"
    return jsonify({"message": f"OTP sent to registered number ending with {masked[-2:]}."})


@app.route("/api/verify-otp", methods=["POST"])
def verify_otp_route():
    if not allocation_done:
        return jsonify({"error": "Results are not published yet."}), 400

    payload = request.get_json() or {}
    try:
        rank = int(payload["rank"])
        otp = int(payload["otp"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Valid rank and OTP are required."}), 400

    if not verify_otp(rank, otp):
        return jsonify({"error": "Wrong OTP. Please try again."}), 401

    clear_otp(rank)
    result = get_student_result(rank, students_data, seat_allocated)
    return jsonify({"message": "OTP verified successfully.", "result": result})


@app.route("/api/download-results")
def download_results():
    if not allocation_done or not os.path.exists(placement_file):
        return jsonify({"error": "Results file is not available yet."}), 404

    return send_file(
        placement_file,
        as_attachment=True,
        download_name="students_placement.txt",
        mimetype="text/plain",
    )


@app.route("/api/status")
def status():
    return jsonify(
        {
            "student_count": len(students_data),
            "allocation_done": allocation_done,
            "sorting_algorithm": sorting_algorithm_used,
            "seats_filled": len(seat_allocated),
        }
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
