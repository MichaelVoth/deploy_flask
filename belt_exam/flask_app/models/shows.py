from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user

class Show:
    DB = "tv_shows_schema"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.created_by_id = data['created_by_id']
        self.creator = None


    @staticmethod
    #checks form data
    def validate_show(show):
        is_valid = True
        if len(show['title']) < 3:
            flash(
                "Title must have at least 3 characters", 'add')
            is_valid = False
        if len(show['network']) < 3:
            flash(
                "Network must have at least 3 characters", 'add')
            is_valid = False
        if len(show['description']) < 3:
            flash('Description must have at least 3 characters', 'add')
            is_valid = False
        if not show['release_date']:
            flash('Must include release date', 'add')
            is_valid = False

        return is_valid

#CREATE
    @classmethod
    #saves show
    def save(cls, data):
        query = '''INSERT INTO tv_shows (title, network, release_date, description, created_by_id)
                VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s,  %(created_by_id)s);'''
        return connectToMySQL(cls.DB).query_db(query, data)
    

#READ
    @classmethod
    #gets all shows
    def get_all_shows(cls):
        query = "SELECT * FROM tv_shows;"
        results = connectToMySQL(cls.DB).query_db(query)
        shows = []
        for a_show in results:
            shows.append(cls(a_show))
        return shows
    

    @classmethod
    #gets show by id and connects creator
    def get_by_id(cls, id):
        query = '''SELECT * FROM tv_shows
                    JOIN users on users.id = created_by_id 
                    WHERE tv_shows.id = %(id)s;'''
        
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        for show in results:
            show_obj = cls(show)
            user_data = {
                "id": show["users.id"],
                "first_name": show["first_name"],
                "last_name": show["last_name"],
                "email": show["email"],
                "password": show["password"],
                "created_at": show["users.created_at"],
                "updated_at": show["users.updated_at"]
            }
            show_obj.creator = user.User(user_data)
        return show_obj


    @classmethod
    #gets how many users liked show
    def get_likes_count(cls, id):
        query = '''SELECT COUNT(*) as likes_count FROM liked_shows WHERE tv_show_id = %(id)s;'''
        data = {'id': id}
        likes_count = connectToMySQL(cls.DB).query_db(query, data)[0]['likes_count']
        return likes_count


#UPDATE
    @classmethod
    #updates show info
    def update_show_info(cls,data):
        query = '''UPDATE tv_shows SET
                    title = %(title)s,
                    network = %(network)s,
                    release_date = %(release_date)s,
                    description = %(description)s
                    WHERE id = %(id)s;'''
        
        return connectToMySQL(cls.DB).query_db(query,data)
    
#DELETE
    @classmethod
    #deletes show
    def delete_show(cls, id):
        query  = "DELETE FROM tv_shows WHERE id = %(id)s;"
        
        return connectToMySQL(cls.DB).query_db(query, {"id": id}) 
