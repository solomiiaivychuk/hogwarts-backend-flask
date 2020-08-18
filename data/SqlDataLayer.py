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

    def add_admin(self, data):
        email = data['email']
        password = data['password']
        cursor = self.__sqlDb.cursor()
        try:
            self.__sqlDb.start_transaction()
            sql = "INSERT INTO admins (email, password) VALUES (%s, %s)"
            values = (email, password)
            cursor.execute(sql, values)
            self.__sqlDb.commit()
            return cursor.rowcount
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
            self.__sqlDb.start_transaction()
            results = []
            sql = "SELECT email, first_name, last_name FROM hogwarts.students"
            cursor.execute(sql)
            for(email, first_name, last_name) in cursor:
                results.append({"email": email, "first_name": first_name, "last_name": last_name})
            return results
        finally:
            cursor.close()


    def get_students_with_skills(self):
        cursor = self.__sqlDb.cursor()
        try:
            self.__sqlDb.start_transaction()
            results = []
            all_data_sql = "SELECT DISTINCT id, email, first_name, last_name, " \
                           "creation_time, update_time, " \
                           "existing_skills.skill_name existing_skill_name, " \
                           "existing_skills.skill_level existing_skill_level, " \
                           "desired_skills.skill_name desired_skill_name " \
                           "FROM hogwarts.students " \
                           "INNER JOIN hogwarts.existing_skills " \
                           "ON students.id = existing_skills.student_id " \
                           "INNER JOIN hogwarts.desired_skills " \
                           "ON students.id = desired_skills.student_id"

            cursor.execute(all_data_sql)
            for (student_id, email, first_name, last_name, creation_time, update_time, existing_skill_name,
                 existing_skill_level, desired_skill_name) in cursor:
                new_student = Student.from_db(email, first_name, last_name, creation_time, update_time,
                                              existing_skill_name, desired_skill_name)
                print(new_student)
                results.append({"id": student_id, "email": email, "first_name": first_name, "last_name": last_name,
                                "creation_time": creation_time, "update_time": update_time,
                                "existing_skills_name": existing_skill_name,
                                "existing_skill_level": existing_skill_level,
                                "desired_skills": desired_skill_name})
            return results
        finally:
            cursor.close()

    def get_student_by_email(self, email):
        cursor = self.__sqlDb.cursor()
        try:
            result = None
            sql = "SELECT email, first_name, last_name, " \
                  "existing_skills.skill_name existing_skill_name, " \
                  "existing_skills.skill_level existing_skill_level, " \
                  "desired_skills.skill_name desired_skill_name " \
                  "FROM hogwarts.students " \
                  "INNER JOIN hogwarts.existing_skills " \
                  "ON students.id = existing_skills.student_id " \
                  "INNER JOIN hogwarts.desired_skills " \
                  "ON students.id = desired_skills.student_id " \
                  "WHERE email = %s;"
            value = (email,)
            cursor.execute(sql, value)
            for (email, first_name, last_name, existing_skill_name, existing_skill_level, desired_skill_name) in cursor:
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

    def get_list_of_students_having_specific_skill(self, skill):
        try:
            results = []
            cursor = self.__sqlDb.cursor()
            sql = "SELECT email from hogwarts.students " \
                  "JOIN hogwarts.existing_skills " \
                  "ON existing_skills.student_id = students.id " \
                  "WHERE skill_name = %s"
            value = (skill,)
            cursor.execute(sql, value)
            for (email) in cursor:
                results.append({"email": email})
            return results
        finally:
            cursor.close()

    def get_list_of_students_wanting_specific_skill(self, skill):
        try:
            results = []
            cursor = self.__sqlDb.cursor()
            sql = "SELECT email from hogwarts.students " \
                  "JOIN hogwarts.desired_skills " \
                  "ON desired_skills.student_id = students.id " \
                  "WHERE skill_name = %s"
            value = (skill,)
            cursor.execute(sql, value)
            for (email) in cursor:
                results.append({"email": email})
            return results
        finally:
            cursor.close()



    def get_num_of_students_having_specific_skill(self, skill):
        cursor = self.__sqlDb.cursor()
        try:
            sql = "SELECT COUNT(student_id) FROM hogwarts.existing_skills " \
                  "WHERE existing_skills.skill_name = %s"
            value = (skill,)
            cursor.execute(sql, value)
            for num in cursor:
                return num
        finally:
            cursor.close()

    def get_num_of_students_wanting_specific_skill(self, skill):
        cursor = self.__sqlDb.cursor()
        try:
            sql = "SELECT COUNT(student_id) FROM hogwarts.desired_skills " \
                  "WHERE desired_skills.skill_name = %s"
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
            sql = "SELECT email " \
                  "FROM hogwarts.students " \
                  "WHERE students.creation_time LIKE %s"
            value = (query_date,)
            cursor.execute(sql, value)
            for (email) in cursor:
                results.append({"email": email})
            return results
        finally:
            cursor.close()

    def get_all_desired_skills(self):
        cursor = self.__sqlDb.cursor()
        try:
            self.__sqlDb.start_transaction()
            results = []
            sql = "SELECT skill_name, COUNT(skill_name) count " \
                  "FROM hogwarts.desired_skills " \
                  "GROUP BY skill_name"
            cursor.execute(sql)
            for (skill_name, count) in cursor:
                results.append({"name": skill_name, "value": count})
            return results
        finally:
            cursor.close()

