from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = "tv_shows_schema"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    #Checks if form data is correctle inputed.
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3 or not str.isalpha(user['first_name']):
            flash(
                "First name must be at least 2 characters and contain only letters.", 'register')
            is_valid = False
        if len(user['last_name']) < 3 or not str.isalpha(user['last_name']):
            flash(
                "Last name must be at least 2 characters and contain only letters.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'register')
            is_valid = False
        if not len(user['password']) >= 9:
            flash('Invalid password. Must contain at least 8 characters.', 'register')
            is_valid = False
        if not str.isalpha(user['password']) == False:
            flash('Password must contain at least 1 number', 'register')
            is_valid = False
        if not str.islower(user['password']) == False:
            flash("Password must contain at least 1 capital letter", 'register')
            is_valid = False
        if not user['password'] == user['confirm_password']:
            flash('Passwords must match', 'register')
            is_valid = False

        return is_valid


#CREATE
    @classmethod
    #Saves user
    def save(cls, data):
        query = '''INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'''
        return connectToMySQL(cls.DB).query_db(query, data)
    

    @classmethod
    #Adds user and show to the likes table
    def like_show(cls, data):
        query = '''INSERT INTO liked_shows (user_id, tv_show_id)
                    VALUES (%(user_id)s, %(tv_show_id)s);'''
        return connectToMySQL(cls.DB).query_db(query, data)


#READ
    @classmethod
    #Gets user by email
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])


    @classmethod
    #gets user by id
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        
        return cls(result[0])
    

    @classmethod
    #gets all the liked shows and users
    def get_likes(cls, id):
        query = "SELECT * FROM liked_shows WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, {'id':id})
        liked_shows = {}
        for a_like in results:
            liked_shows[a_like['tv_show_id']] = a_like['user_id']
        return liked_shows


#DELETE
    @classmethod
    def unlike_show(cls, data):
        query  = "DELETE FROM liked_shows WHERE user_id = %(user_id)s AND tv_show_id = %(tv_show_id)s;"
        
        return connectToMySQL(cls.DB).query_db(query, data) 