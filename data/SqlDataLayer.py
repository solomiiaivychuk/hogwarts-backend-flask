import mysql.connector
from decouple import config
from flask import json

from data.DataLayer import DataLayer


class SqlDataLayer(DataLayer):

    def __init__(self):
        super().__init__()
        self.__connect()

    def __connect(self):
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
        cursor = self.__sqlDb.cursor()
        try:
            results = []
            sql = "SELECT * FROM admins"
            cursor.execute(sql)
            for (admin_id, email, password) in cursor:
                results.append({"id": admin_id, "email": email, "password": password})
            return results
        finally:
            cursor.close()

    def login_admin(self, data):
        email = data["email"]
        password = data["password"]
        cursor = self.__sqlDb.cursor()
        try:
            result = None
            sql = "SELECT email FROM admins WHERE email = '%s' AND password = '%s'"
            cursor.execute(sql)
            for email in cursor:
                result = {'email': email}
            return result
        finally:
            cursor.close()

    def get_students(self):
        cursor = self.__sqlDb.cursor()
        try:
            results = []
            sql = "SELECT * FROM students"
            cursor.execute(sql)
            for (student_id, email, first_name, last_name) in cursor:
                results.append({"id": student_id, "email": email, "first_name": first_name, "last_name": last_name})
            return results
        finally:
            cursor.close()

    def add_student(self, content):
        print(content)
        email = content['email']
        first_name = content['first_name']
        last_name = content['last_name']
        cursor = self.__sqlDb.cursor()
        try:
            self.__sqlDb.start_transaction()
            sql = "INSERT INTO students (email, first_name, last_name) VALUES (%s, %s, %s)"
            value = (email, first_name, last_name)
            cursor.execute(sql, value)
            self.__sqlDb.commit()
            print(cursor.rowcount, "Inserted successfully")
            return cursor.rowcount
        finally:
            cursor.close()

    def remove_student(self, email):
        cursor = self.__sqlDb.cursor()
        try:
            self.__sqlDb.start_transaction()
            sql = "DELETE FROM students WHERE email = %s"
            value = (email,)
            cursor.execute(sql, value)
            self.__sqlDb.commit()
            print(cursor.rowcount, "Deleted successfully")
            return cursor.rowcount
        finally:
            cursor.close()

