import mysql.connector
from decouple import config
from flask import json
from data.Student import Student

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
            sql = "SELECT email FROM admins WHERE email = %s AND password = %s"
            value = (email, password)
            cursor.execute(sql, value)
            for (email) in cursor:
                result = {'email': email}
            return result
        finally:
            cursor.close()

    def get_students(self):
        cursor = self.__sqlDb.cursor()
        try:
            results = []
            """
            all_data_sql = "SELECT * FROM hogwarts.students " \
                           "LEFT JOIN hogwarts.existing_skills " \
                           "ON students.id = existing_skills.student_id " \
                           "LEFT JOIN hogwarts.desired_skills " \
                           "ON students.id = desired_skills.student_id"
            """
            students_sql = "SELECT * FROM hogwarts.students"
            cursor.execute(students_sql)

            for (student_id, email, first_name, last_name, creation_time, update_time) in cursor:

                ex_skills_arr = []
                desired_skills_arr = []

                ex_skills_sql = "SELECT skill_name, skill_level FROM hogwarts.existing_skills WHERE student_id = %s"
                value = (student_id,)
                cursor.execute(ex_skills_sql, value)
                for(skill_name, skill_level) in cursor:
                    ex_skills_arr.append({"skill_name": skill_name, "skill_level": skill_level})

                des_skills_sql = "SELECT skill_name FROM hogwarts.desired_skills WHERE student_id = %s"
                value = (student_id,)
                cursor.execute(des_skills_sql, value)
                for (skill_name) in cursor:
                    desired_skills_arr.append({"skill_name": skill_name})

                results.append({"id": student_id, "email": email, "first_name": first_name, "last_name": last_name,
                                "creation_time": creation_time, "update_time": update_time,
                                "existing_skills": ex_skills_arr, "desires_skills": desired_skills_arr})
            return results
        finally:
            cursor.close()

    def get_student_by_email(self, email):
        cursor = self.__sqlDb.cursor()
        try:
            result = None
            sql = "SELECT email, first_name, last_name FROM students WHERE email = %s"
            value = (email,)
            cursor.execute(sql, value)
            for (email, first_name, last_name) in cursor:
                result = {"email": email, "first_name": first_name, "last_name": last_name}
            return result
        finally:
            cursor.close()

    def add_student(self, content):
        email = content['email']
        first_name = content['first_name']
        last_name = content['last_name']
        existing_skills_arr = content['existing_skills']
        desired_skills_arr = content['desired_skills']
        new_student = Student.from_json(email, first_name, last_name, existing_skills_arr, desired_skills_arr)
        creation_time = new_student.get_creation_time()
        update_time = new_student.get_update_time()
        cursor = self.__sqlDb.cursor()
        try:
            self.__sqlDb.start_transaction()
            student_sql = "INSERT INTO students (email, first_name, last_name, creation_time, update_time)" \
                          " VALUES (%s, %s, %s, %s, %s)"
            student_value = (email, first_name, last_name, creation_time, update_time)
            cursor.execute(student_sql, student_value)
            self.__sqlDb.commit()
            stud_id = cursor.lastrowid
            for skill in existing_skills_arr:
                ex_skills_sql = "INSERT INTO existing_skills (student_id, skill_name, skill_level) VALUES (%s, %s, %s)"
                ex_skills_value = (stud_id, skill['name'], skill['level'])
                cursor.execute(ex_skills_sql, ex_skills_value)
                self.__sqlDb.commit()
            for skill in desired_skills_arr:
                des_skills_sql = "INSERT INTO desired_skills (student_id, skill_name) VALUES (%s, %s)"
                des_skills_value = (stud_id, skill['name'])
                cursor.execute(des_skills_sql, des_skills_value)
                self.__sqlDb.commit()
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

    def get_num_of_students_having_specific_skill(self, skill):
        cursor = self.__sqlDb.cursor()
        try:
            sql = "SELECT COUNT(student_id) from hogwarts.existing_skills WHERE existing_skills.skill_name = %s"
            value = (skill,)
            cursor.execute(sql, value)
            for num in cursor:
                return num
        finally:
            cursor.close()

    def get_num_of_students_wanting_specific_skill(self, skill):
        cursor = self.__sqlDb.cursor()
        try:
            sql = "SELECT COUNT(student_id) from hogwarts.desired_skills WHERE desired_skills.skill_name = %s"
            value = (skill,)
            cursor.execute(sql, value)
            for num in cursor:
                return num
        finally:
            cursor.close()

    def get_students_added_on_date(self, date):
        cursor = self.__sqlDb.cursor()
        query_date = str.format(date+'%')
        try:
            results = []
            sql = "SELECT first_name, last_name, creation_time FROM hogwarts.students WHERE students.creation_time LIKE %s"
            value = (query_date,)
            cursor.execute(sql, value)
            for (first_name, last_name, creation_time) in cursor:
                results.append({"first_name": first_name, "last_name": last_name, "creation_time": creation_time})
            return results
        finally:
            cursor.close()
