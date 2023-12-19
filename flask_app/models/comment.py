from flask_app.config.mysqlconnections import connectToMySQL
from flask_app.models import post, user
from flask import flash

class Comment:
    DB = "dojo_wall"
    def __init__( self , data ):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.creator = None

    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO comments (content, user_id, post_id)
                VALUES (%(content)s, %(user_id)s, %(post_id)s);
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    