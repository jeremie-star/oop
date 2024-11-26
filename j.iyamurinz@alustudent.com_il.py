class Assignment:
    def __init__(self, name, type_, score, weight):
        self.name = name
        self.type = type_  # "FA" for Formative or "SA" for Summative
        self.score = score
        self.weight = weight

    def is_below_passing_score(self, passing_score=50):
        return self.score < passing_score


class Student:
    def __init__(self):
        self.assignments = []

    def add_assignment(self, name, type_, score, weight):
        self.assignments.append(Assignment(name, type_, score, weight))

    def input_assignments(self):
        print("Enter assignment details. Type 'done' when finished.")
        while True:
            name = input("Assignment Name (or 'done' to finish): ")
            if name.lower() == "done":
                break
            type_ = input("Type (FA for Formative, SA for Summative): ").upper()
            while type_ not in ["FA", "SA"]:
                type_ = input("Invalid type. Enter FA or SA: ").upper()
            score = float(input("Score (0-100): "))
            weight = float(input("Weight (%) FA=60 and SA=40 max: "))
            self.add_assignment(name, type_, score, weight)

    def calculate_scores(self):
        scores = {"FA": 0, "SA": 0}
        weights = {"FA": 0, "SA": 0}

        for a in self.assignments:
            scores[a.type] += a.score * a.weight / 100
            weights[a.type] += a.weight

        if weights["FA"] > 60 or weights["SA"] > 40:
            raise ValueError("Weights exceed allowed limits: 60% for formative, 40% for summative")

        return scores["FA"], scores["SA"]

    def check_progression(self):
        formative_total, summative_total = self.calculate_scores()
        return "Passed" if formative_total >= 30 and summative_total >= 20 else "Failed"

    def resubmission_eligibility(self):
        eligible_assignments = [a for a in self.assignments if a.type == "FA" and a.is_below_passing_score()]
        if not eligible_assignments:
            return []
        lowest_score = min(a.score for a in eligible_assignments)
        return [a for a in eligible_assignments if a.score == lowest_score]

    def generate_transcript(self, order="asc"):
        sorted_assignments = sorted(
            self.assignments,
            key=lambda a: a.score,
            reverse=(order == "des")
        )

        print(f"Transcript Breakdown ({order.capitalize()} Order):")
        print(f"{'Assignment':<18} {'Type':<15} {'Score (%)':<12} {'Weight (%)':<12}")
        print("-" * 50)
        for a in sorted_assignments:
            print(f"{a.name:<18} {a.type:<15} {a.score:<12} {a.weight:<12}")
        print("-" * 50)


# Main Program
def main():
    student = Student()

    # Input assignments
    student.input_assignments()

    try:
        # Calculate and display scores
        formative_total, summative_total = student.calculate_scores()
        print(f"Formative Total: {formative_total}%, Summative Total: {summative_total}%")
        print("Course Progression:", student.check_progression())

        # Check resubmission eligibility
        eligible_for_resubmission = student.resubmission_eligibility()
        if eligible_for_resubmission:
            print("Eligible for resubmission:")
            for a in eligible_for_resubmission:
                print(f"{a.name} with score {a.score}%")
        else:
            print("No assignments eligible for resubmission.")

        # Generate transcript
        order = input("Enter transcript order type 'asc' if is ascending and 'des' if it is deseding): ").lower()
        while order not in ["asc", "des"]:
            order = input("Invalid order. Enter asc or des: ").lower()
        student.generate_transcript(order=order)

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
