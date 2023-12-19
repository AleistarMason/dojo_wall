from flask_app.config.mysqlconnections import connectToMySQL
from flask_app.models import comment, user
from flask import flash


class Post:
    DB = "dojo_wall"
    def __init__( self , data ):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.creator = None
        self.comments = []
    
    @classmethod
    def new_post(cls, data):
        query = """
                INSERT INTO posts (content, user_id)
                VALUES (%(content)s, %(user_id)s);
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def get_all_posts_with_creator(cls):
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC"
        results = connectToMySQL(cls.DB).query_db(query)
        #empty list that will hold all the post data
        all_posts = []
        for row in results:
            #creates an instance of post for each post in the db
            one_post = cls(row)
            #also writes the user info for each post
            creator_info = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            #saves the user info into a user class before adding it to the post's creator variable
            creator = user.User(creator_info)
            one_post.creator = creator
            #appends all posts into the list
            all_posts.append(one_post)
        return all_posts

    @classmethod
    def get_comments(cls, id):
        query = "SELECT * FROM posts JOIN comments ON comments.post_id = posts.id JOIN users ON comments.user_id = users.id WHERE posts.id = %(id)s ORDER BY comments.created_at ASC;"
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        comments = []
        for row in results:
            comment_info = {
                'id': row['comments.id'],
                'content': row['comments.content'],
                'created_at': row['comments.created_at'],
                'updated_at': row['comments.updated_at']
            }
            creator_info = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            one_comment = comment.Comment(comment_info)
            one_comment.creator = user.User(creator_info)
            comments.append(one_comment)
        return comments
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)