import sqlite3

connection = sqlite3.connect("job_tracker.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    Application_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Company TEXT NOT NULL,
    Job_Role TEXT NOT NULL,
    Experience TEXT NOT NULL,
    Qualification TEXT NOT NULL,
    Application_Date TEXT NOT NULL,
    Status TEXT NOT NULL
)
""")

connection.commit()

statuses = [
    "Applied",
    "Under Review",
    "Interview",
    "Selected",
    "Rejected"
]

while True:

    print("\n===== JOB APPLICATION TRACKER =====")
    print("1. Add Application")
    print("2. View Applications")
    print("3. Update Status")
    print("4. Search Application")
    print("5. Delete Application")
    print("6. Dashboard")
    print("7. Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        continue

    # ==================================================
    # 1. ADD APPLICATION
    # ==================================================

    if choice == 1:

        try:
            n = int(input("How many applications? "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        if n <= 0:
            print("Please enter a number greater than 0!")
            continue

        for i in range(n):

            print(f"\n--- Application {i + 1} ---")

            Company = input("Enter company name: ").strip()
            Job_Role = input("Enter job role: ").strip()
            Experience = input("Enter your experience: ").strip()
            Qualification = input("Enter your qualification: ").strip()
            Application_Date = input("Enter application date: ").strip()

            if not Company or not Job_Role or not Experience or not Qualification or not Application_Date:
                print("All fields are required!")
                continue

            print("\nAvailable Status:")

            for status in statuses:
                print(status)

            Status = input("Enter your application status: ").strip()

            valid_status = None

            for status in statuses:
                if Status.casefold() == status.casefold():
                    valid_status = status
                    break

            if valid_status is None:
                print("Invalid status!")
                continue

            cursor.execute("""
            INSERT INTO applications
            (
                Company,
                Job_Role,
                Experience,
                Qualification,
                Application_Date,
                Status
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                Company,
                Job_Role,
                Experience,
                Qualification,
                Application_Date,
                valid_status
            ))

            connection.commit()

            print("Application added successfully!")

    # ==================================================
    # 2. VIEW APPLICATIONS
    # ==================================================

    elif choice == 2:

        cursor.execute("""
        SELECT *
        FROM applications
        ORDER BY Application_ID
        """)

        applications = cursor.fetchall()

        if not applications:
            print("No applications available!")

        else:

            print("\n===== APPLICATIONS =====")

            for number, application in enumerate(applications, start=1):

                print("Application Number:", number)
                print("Application ID:", application[0])
                print("Company:", application[1])
                print("Job Role:", application[2])
                print("Experience:", application[3])
                print("Qualification:", application[4])
                print("Application Date:", application[5])
                print("Status:", application[6])
                print()

    # ==================================================
    # 3. UPDATE STATUS
    # ==================================================

    elif choice == 3:

        cursor.execute("""
        SELECT *
        FROM applications
        ORDER BY Application_ID
        """)

        applications = cursor.fetchall()

        if not applications:
            print("No applications available!")

        else:

            print("\n===== APPLICATIONS =====")

            for number, application in enumerate(applications, start=1):

                print(
                    number,
                    "-",
                    application[1],
                    "-",
                    application[2],
                    "-",
                    application[6]
                )

            try:
                update_choice = int(
                    input("Enter application number: ")
                )
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue

            if update_choice < 1 or update_choice > len(applications):
                print("Invalid application number!")

            else:

                application_id = applications[
                    update_choice - 1
                ][0]

                print("\nAvailable Status:")

                for status in statuses:
                    print(status)

                new_status = input(
                    "Enter new status: "
                ).strip()

                valid_status = None

                for status in statuses:

                    if new_status.casefold() == status.casefold():
                        valid_status = status
                        break

                if valid_status is None:
                    print("Invalid status!")

                else:

                    cursor.execute("""
                    UPDATE applications
                    SET Status = ?
                    WHERE Application_ID = ?
                    """, (
                        valid_status,
                        application_id
                    ))

                    connection.commit()

                    print("Status updated successfully!")

    # ==================================================
    # 4. SEARCH APPLICATION
    # ==================================================

    elif choice == 4:

        while True:

            print("\n===== SEARCH APPLICATION =====")
            print("1. Search by Company")
            print("2. Search by Job Role")
            print("3. Search by Status")
            print("4. Back")

            try:
                search_choice = int(
                    input("Enter your choice: ")
                )
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue

            # SEARCH BY COMPANY

            if search_choice == 1:

                search_company = input(
                    "Enter company name to search: "
                ).strip()

                if not search_company:
                    print("Please enter a company name!")
                    continue

                cursor.execute("""
                SELECT *
                FROM applications
                WHERE LOWER(Company) LIKE LOWER(?)
                ORDER BY Application_ID
                """, (
                    "%" + search_company + "%",
                ))

            # SEARCH BY JOB ROLE

            elif search_choice == 2:

                search_role = input(
                    "Enter job role to search: "
                ).strip()

                if not search_role:
                    print("Please enter a job role!")
                    continue

                cursor.execute("""
                SELECT *
                FROM applications
                WHERE LOWER(Job_Role) LIKE LOWER(?)
                ORDER BY Application_ID
                """, (
                    "%" + search_role + "%",
                ))

            # SEARCH BY STATUS

            elif search_choice == 3:

                print("\nAvailable Status:")

                for status in statuses:
                    print(status)

                search_status = input(
                    "Enter status to search: "
                ).strip()

                valid_status = None

                for status in statuses:

                    if search_status.casefold() == status.casefold():
                        valid_status = status
                        break

                if valid_status is None:
                    print("Invalid status!")
                    continue

                cursor.execute("""
                SELECT *
                FROM applications
                WHERE Status = ?
                ORDER BY Application_ID
                """, (
                    valid_status,
                ))

            # BACK

            elif search_choice == 4:
                break

            else:
                print("Invalid choice! Please enter 1 to 4.")
                continue

            # DISPLAY RESULTS

            if search_choice in (1, 2, 3):

                search_results = cursor.fetchall()

                if not search_results:

                    print("Application not found!")

                else:

                    print("\n===== SEARCH RESULTS =====")

                    for application in search_results:

                        print("Application ID:", application[0])
                        print("Company:", application[1])
                        print("Job Role:", application[2])
                        print("Experience:", application[3])
                        print("Qualification:", application[4])
                        print("Application Date:", application[5])
                        print("Status:", application[6])
                        print()

    # ==================================================
    # 5. DELETE APPLICATION
    # ==================================================

    elif choice == 5:

        cursor.execute("""
        SELECT *
        FROM applications
        ORDER BY Application_ID
        """)

        applications = cursor.fetchall()

        if not applications:

            print("No applications available!")

        else:

            print("\n===== APPLICATIONS =====")

            for number, application in enumerate(applications, start=1):

                print(
                    number,
                    "-",
                    application[1],
                    "-",
                    application[2]
                )

            try:
                delete_choice = int(
                    input("Enter application number: ")
                )
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue

            if delete_choice < 1 or delete_choice > len(applications):

                print("Invalid application number!")

            else:

                application_id = applications[
                    delete_choice - 1
                ][0]

                cursor.execute("""
                DELETE FROM applications
                WHERE Application_ID = ?
                """, (
                    application_id,
                ))

                connection.commit()

                print("Application deleted successfully!")

    # ==================================================
    # 6. DASHBOARD
    # ==================================================

    elif choice == 6:

        cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        """)

        total = cursor.fetchone()[0]

        print("\n===== DASHBOARD =====")
        print("Total Applications:", total)

        for status in statuses:

            cursor.execute("""
            SELECT COUNT(*)
            FROM applications
            WHERE Status = ?
            """, (
                status,
            ))

            count = cursor.fetchone()[0]

            print(f"{status}: {count}")

    # ==================================================
    # 7. EXIT
    # ==================================================

    elif choice == 7:

        print("Thank you for using Job Application Tracker!")

        connection.close()
        break

    # ==================================================
    # INVALID CHOICE
    # ==================================================

    else:

        print(
            "Invalid choice! Please enter a number between 1 and 7."
        )