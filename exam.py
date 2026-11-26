
import mysql.connector
from datetime import datetime


class Hospital_db:

    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                user='root',
                password='root',
                host='localhost',
                database='hospital_management'
            )
            print("Successfully connected to database")

        except :

            print("Failed to connect")


    def register(self, patient_name, age, phone, department,
                 doctor_name, appointment_date):
        try:
            if age <= 0 or age > 120:
                print("Invalid age")
                return

            datetime.strptime(appointment_date, "%Y-%m-%d")

            cursor = self.conn.cursor()

            query = """
            INSERT INTO patients
            (patient_name, age, phone, department,
             doctor_name, appointment_date)
            VALUES(%s, %s, %s, %s, %s, %s)
            """

            data = (
                patient_name, age, phone,
                department, doctor_name, appointment_date
            )

            cursor.execute(query, data)
            self.conn.commit()

            print("Patient registered successfully")
            cursor.close()

        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD")

        except mysql.connector.Error as e:
            print("Failed to register:", e)


    def view_appointments(self, start_date, end_date):
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")

            cursor = self.conn.cursor()

            query = """
            SELECT * FROM patients
            WHERE appointment_date BETWEEN %s AND %s
            ORDER BY appointment_date ASC
            """

            data = (start_date, end_date)

            cursor.execute(query, data)

            records = cursor.fetchall()

            if records:
                for row in records:
                    print(row)
            else:
                print("No appointments found")



        except ValueError:
            print("Invalid date format")

        except:
            print("Failed to view appointments:")


    def search(self, value):
        try:
            cursor = self.conn.cursor()

            query = """
            SELECT * FROM patients
            WHERE patient_id = %s
            OR patient_name LIKE %s
            OR doctor_name LIKE %s
            """

            data = (
                value,
                '%' + value + '%',
                '%' + value + '%'
            )

            cursor.execute(query, data)

            records = cursor.fetchall()

            if records:
                for row in records:
                    print(row)
            else:
                print("No records found")



        except:
            print("Failed to search:")


    def update(self, patient_id, new_date):
        try:
            datetime.strptime(new_date, "%Y-%m-%d")

            cursor = self.conn.cursor()

            query = """
            UPDATE patients
            SET appointment_date = %s
            WHERE patient_id = %s
            """

            data = (new_date, patient_id)

            cursor.execute(query, data)
            self.conn.commit()

            if cursor.rowcount > 0:
                print("Updated successfully")
            else:
                print("No records found or date unchanged")




        except:
            print("Failed to update:")


    def delete(self, patient_id):
        try:


                cursor = self.conn.cursor()

                query = """
                DELETE FROM patients
                WHERE patient_id = %s
                """

                data = (patient_id,)

                cursor.execute(query, data)
                self.conn.commit()

                if cursor.rowcount > 0:
                    print("Deleted successfully")
                else:
                    print("No records found")





        except:
            print("Failed to delete")


    def summary(self):
        try:
            cursor = self.conn.cursor()

            query = """
            SELECT COUNT(*), AVG(age)
            FROM patients
            """

            cursor.execute(query)

            result = cursor.fetchone()

            print("Total number of patients:", result[0])
            print("Average age of patients:", result[1])

            query = """
            SELECT department, COUNT(*)
            FROM patients
            GROUP BY department
            """

            cursor.execute(query)

            records = cursor.fetchall()

            print("\nDepartment-wise patient count:")

            for row in records:
                print("Department:", row[0],
                      "Total patients:", row[1])



        except:
            print("Summary failed:")



b = Hospital_db()

if b.conn:

    while True:

        print("\n------ HOSPITAL MANAGEMENT ------")
        print("1. Register Patient")
        print("2. View Appointments")
        print("3. Search Patient")
        print("4. Update Appointment")
        print("5. Delete Patient")
        print("6. Summary")
        print("7. Exit")

        try:
            ch = int(input("Enter your choice: "))

            if ch == 1:
                name = input("Enter patient name: ")
                age = int(input("Enter age: "))
                phone = input("Enter phone: ")
                department = input("Enter department: ")
                doctor = input("Enter doctor name: ")
                date = input("Enter appointment date (YYYY-MM-DD): ")

                b.register(name, age, phone, department, doctor, date)

            elif ch == 2:
                start = input("Enter start date (YYYY-MM-DD): ")
                end = input("Enter end date (YYYY-MM-DD): ")

                b.view_appointments(start, end)

            elif ch == 3:
                value = input("Enter patient ID, name or doctor name: ")
                b.search(value)

            elif ch == 4:
                patient_id = int(input("Enter patient ID: "))
                new_date = input("Enter new appointment date (YYYY-MM-DD): ")

                b.update(patient_id, new_date)

            elif ch == 5:
                patient_id = int(input("Enter patient ID: "))
                b.delete(patient_id)

            elif ch == 6:
                b.summary()

            elif ch == 7:
                print("Program exited")
                break

            else:
                print("Invalid choice")
                break

        except ValueError:
            print("Invalid input")
            break

    b.conn.close()




















