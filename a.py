import random
print(random.randrange(16,19))
def generate_attendance(n, m, target_probability):
    # Calculate the target count for the range 85-90
    target_count = int(n * target_probability)

    # Generate attendance percentages for each student
    attendance_percentages = []
    for _ in range(n):
        # Randomly assign attendance percentage in the range 80-90
        attendance = random.uniform(80, 90)
        attendance_percentages.append(attendance)

    # Sort the attendance percentages
    attendance_percentages.sort()

    # Calculate the difference between the target count and the actual count
    diff = n - target_count

    # Adjust the attendance percentages to achieve the target probability
    for i in range(diff):
        # Randomly select an index to decrease attendance in the range 85-90
        index_to_decrease = random.randint(target_count, n - 1)
        # Decrease attendance in the range 85-90
        attendance_percentages[index_to_decrease] = random.uniform(85, 90)

    return attendance_percentages

# Example usage with n = 100 students, m = 20 working days, and target probability = 0.3
n_students = 30
m_working_days = 20
target_probability = 0.3

attendance_percentages = generate_attendance(n_students, m_working_days, target_probability)

# Display the generated attendance percentages
print("Generated Attendance Percentages:")
for i, attendance in enumerate(attendance_percentages, 1):
    print(f"Student {i}: {attendance:.2f}%")