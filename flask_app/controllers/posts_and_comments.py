from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.comment import Comment
from flask_app import app

@app.route('/post', methods=['POST'])
def create_post():
    if not request.form.get('content'):
        flash('Post content must not be blank', 'post')
        return redirect('/dashboard')
    data = {
        'content': request.form['content'],
        'user_id': session['user_id']
    }
    Post.new_post(data)
    return redirect('/dashboard')

@app.route('/delete', methods=['POST'])
def delete():
    Post.delete(request.form)
    return redirect('/dashboard')

@app.route('/comment', methods=['POST'])
def comment():
    if not request.form.get('content'):
        flash('comment must not be blank', 'comment')
        return redirect('/dashboard')
    data = {
        'content': request.form['content'],
        'post_id': int(request.form['post_id']),
        'user_id': int(session['user_id'])
    }
    Comment.save(data)
    return redirect('/dashboard')