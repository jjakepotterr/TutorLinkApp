# tutor_search_and_rate.py

class Tutor:
    def __init__(self, name, subject, ratings=None, comments=None):
        self.name = name
        self.subject = subject
        self.ratings = ratings if ratings else []
        self.comments = comments if comments else []

    def add_rating(self, stars, comment):
        if 1 <= stars <= 5:
            self.ratings.append(stars)
            self.comments.append(comment)
            print(f"\n✅ Thank you! You rated {self.name} {stars} stars.")
        else:
            print("⚠️ Please enter a valid rating between 1 and 5.")

    def average_rating(self):
        if not self.ratings:
            return 0
        return round(sum(self.ratings) / len(self.ratings), 2)

    def show_profile(self):
        print("\n------------------------------")
        print(f"Tutor: {self.name}")
        print(f"Subject: {self.subject}")
        print(f"Average Rating: {self.average_rating()}⭐")
        print("Comments:")
        if not self.comments:
            print("No comments yet.")
        else:
            for stars, comment in zip(self.ratings, self.comments):
                print(f"- {stars}⭐: {comment}")
        print("------------------------------\n")


def search_tutor(subject_name, tutors):
    subject_name = subject_name.strip().lower()
    found = [t for t in tutors if subject_name in t.subject.lower()]

    if not found:
        print("\n❌ No tutor found for that subject.\n")
        return None
    else:
        print("\n🔍 Search Results:")
        for i, t in enumerate(found, 1):
            print(f"{i}. {t.name} - {t.subject} ({t.average_rating()}⭐)")
        print()
        return found


def main():
    tutors = [
        Tutor("Dr. Smith", "Calculus 1", [5, 4, 5], ["Very clear!", "Helpful explanations", "Excellent tutor"]),
        Tutor("Ms. Johnson", "Physics", [3, 4, 4], ["Good but a bit fast", "Helpful examples", "Nice personality"]),
        Tutor("Mr. Lee", "Computer Science", [5, 5, 4, 5], ["Great coder!", "Patient", "Explains well", "My favorite tutor"]),
    ]

    while True:
        print("===== Tutor Search & Rating System =====")
        print("1. Search by subject")
        print("2. View all tutors")
        print("3. Exit")
        choice = input("Select an option (1-3): ")

        if choice == "1":
            subject = input("\nEnter the subject name (e.g., Calculus 1, Physics, Computer Science): ")
            results = search_tutor(subject, tutors)
            if results:
                select = input("Enter the number of the tutor to view details or press Enter to go back: ")
                if select.isdigit() and 1 <= int(select) <= len(results):
                    tutor = results[int(select) - 1]
                    tutor.show_profile()

                    rate = input("Would you like to rate this tutor? (y/n): ").lower()
                    if rate == "y":
                        try:
                            stars = int(input("Enter stars (1-5): "))
                            comment = input("Enter your comment: ")
                            tutor.add_rating(stars, comment)
                            print(f"New average rating: {tutor.average_rating()}⭐\n")
                        except ValueError:
                            print("⚠️ Invalid input. Please enter a number between 1 and 5.")

        elif choice == "2":
            print("\nAll Tutors:")
            for t in tutors:
                print(f"- {t.name} ({t.subject}): {t.average_rating()}⭐")
            print()

        elif choice == "3":
            print("Goodbye! 👋")
            break

        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()
