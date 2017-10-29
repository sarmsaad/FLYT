# Calculates wait time for a given person

# Assumptions for check-in:
# per person (or group) check-in time at booth: 3 minutes
# 3 people per team
# 40% of the people do self check-in


def calculate_checkin_time(airline, num_flights, num_seats):
    total_people = num_flights * num_seats

    if total_people < 100:
        wait_time = (0.40 * total_people * 3.0) / 9.0

    elif total_people > 100 and total_people < 200:
        wait_time = (0.40 * total_people * 3.0) / 12.0

    else:
        wait_time = (0.40 * total_people * 3.0) / 15.0

    return wait_time

# assuming a maximum of 50% of the people wait in security lines at a time
# 45 seconds ON AVERAGE per person to get through security

def calculate_security_time(tot_people):
    wait_time = (0.40 * tot_people * 0.75) / 4.0

    return wait_time

total_time = calculate_checkin_time() + calculate_security_time() + 20
