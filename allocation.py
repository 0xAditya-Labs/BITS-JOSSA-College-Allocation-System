from sorting import sort_ranks_random

# Maximum seats: 8 (2x2x2)
# College Codes:
# Pilani CSE : 1
# Goa CSE    : 2
# Pilani ECE : 3
# Goa ECE    : 4

COLLEGE_LIST = [
    (0, 0),
    ("Pilani", "CSE"),
    ("Goa", "CSE"),
    ("Pilani", "ECE"),
    ("Goa", "ECE"),
]

MAX_SEATS = 8


def take_space(text, n):
    return str(text) + " " * (n - len(str(text)))


def add_student(data, name, roll_no, rank, phone_number, choices):
    """Add a student record to the in-memory data store."""
    if rank in data:
        raise ValueError(f"Rank {rank} is already registered.")
    if roll_no in [v[0] for v in data.values()]:
        raise ValueError(f"Roll number {roll_no} is already registered.")

    valid_codes = {1, 2, 3, 4}
    cleaned = [c for c in choices if c in valid_codes]
    if not cleaned:
        raise ValueError("At least one valid college preference (1-4) is required.")

    data[rank] = (roll_no, name, phone_number, cleaned)
    return data


def allocate_seats(data):
    """
    Run seat allocation on registered students.
    Returns sorted ranks, seat allocation map, and the sorting algorithm used.
    """
    ranks_registered = list(data.keys())
    sorted_ranks, algorithm_used = sort_ranks_random(ranks_registered)

    seats_available = [0, 2, 2, 2, 2]
    seat_allocated = {}
    counter = 0

    for rank in sorted_ranks:
        if counter >= MAX_SEATS:
            break

        got_seat = False
        pref_list = data[rank][3]
        for pref_code in pref_list:
            if seats_available[pref_code] > 0:
                got_seat = True
                seat_allocated[rank] = pref_code
                seats_available[pref_code] -= 1
                break

        if got_seat:
            counter += 1

    return sorted_ranks, seat_allocated, algorithm_used


def generate_placement_file(data, sorted_ranks, seat_allocated, filepath="students_placement.txt"):
    """Write allocation results to a downloadable text file."""
    lines = [
        "Rank    Roll Number    Name                Phone Number   College     Branch",
        "",
    ]

    for rank in sorted_ranks:
        roll_no, name, phone, _ = data[rank]
        line = (
            take_space(rank, 8)
            + take_space(roll_no, 15)
            + take_space(name, 20)
            + take_space(phone, 15)
        )

        if rank in seat_allocated:
            colg_code = seat_allocated[rank]
            line += take_space(COLLEGE_LIST[colg_code][0], 12) + COLLEGE_LIST[colg_code][1]
        else:
            line += "NOT QUALIFIED"

        lines.append(line)

    content = "\n".join(lines) + "\n"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return content


def get_student_result(rank, data, seat_allocated):
    """Return report card details for a verified student."""
    if rank not in data:
        return None

    roll_no, name, phone, _ = data[rank]
    result = {
        "rank": rank,
        "roll_no": roll_no,
        "name": name,
        "phone": phone,
        "qualified": rank in seat_allocated,
    }

    if rank in seat_allocated:
        colg_code = seat_allocated[rank]
        result["campus"] = f"BITS {COLLEGE_LIST[colg_code][0]}"
        result["branch"] = COLLEGE_LIST[colg_code][1]
    else:
        result["campus"] = None
        result["branch"] = None
        result["message"] = "Not Qualified. All the best for next time."

    return result
