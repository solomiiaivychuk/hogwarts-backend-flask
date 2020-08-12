import mysql.connector
from decouple import config
from werkzeug.debug import console


class SqlDataLayer:

    def __init__(self):
        self.create()

    def create(self):
        try:
            self.__sqlDb = mysql.connector.connect(
                host="127.0.0.1",
                user=config('MYSQL_USER'),
                password=config('PASSWORD'),
                database='hogwarts'
            )
        except Exception as e:
            print(e)

    def close(self):
        self.__sqlDb.close()

    def get_admins(self):
        try:
            cursor = self.__sqlDb.cursor()
            results = []
            sql = "SELECT * FROM admins"
            cursor.execute(sql)
            for (admin_id, email, password) in cursor:
                results.append({"id": admin_id, "email": email, "password": password})
            return results
        finally:
            cursor.close()

    def get_students(self):
        try:
            cursor = self.__sqlDb.cursor()
            results = []
            sql = "SELECT * FROM students"
            cursor.execute(sql)
            for (student_id, email, first_name, last_name) in cursor:
                results.append({"id": student_id, "email": email, "first_name": first_name, "last_name": last_name})
            return results
        finally:
            cursor.close()

    def add_student(self, id, email, first_name, last_name):
        try:
            cursor = self.__sqlDb.cursor()
            self.__sqlDb.start_transaction()
            sql = "INSERT INTO students (id, email, first_name, last_name) VALUES (%s, %s, %s, %s)"
            value = (id, email, first_name, last_name)
            cursor.execute(sql, value)
            print(cursor.rowcount, "Inserted successfully")
            return cursor.rowcount
        finally:
            cursor.close()

