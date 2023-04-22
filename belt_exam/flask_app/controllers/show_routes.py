from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.shows import Show



@app.route('/shows')
def dashboard_page():
    # Checks if user id is logged in.
    if session.get('user_id') is None:
        return redirect('/')
    # Gets user info by id in session.
    user = User.get_by_id({'id': session['user_id']})
    shows = Show.get_all_shows()
    likes = User.get_likes(session['user_id'])
    print(likes)

    return render_template('shows.html', user=user, shows=shows, likes=likes)



@app.route('/shows/new')
def create_show():
    # Checks if user id is logged in.
    if session.get('user_id') is None:
        return redirect('/')

    return render_template('create.html')


@app.route('/shows/add', methods=['POST'])
def add_show():
    if session.get('user_id') is None:
        return redirect('/')

    # Handles validation of creation.
    if not Show.validate_show(request.form):
        return redirect('/shows/new')

    # Saves show in DB.
    Show.save(request.form)

    return redirect("/shows")


@app.route('/shows/<int:id>')
def view_show(id):
    if session.get('user_id') is None:
        return redirect('/')
    
    show = Show.get_by_id(id)
    likes_count = Show.get_likes_count(id)
    return render_template('view.html', show=show, likes_count=likes_count)


@app.route('/shows/edit/<int:id>')
def edit_show(id):
    if session.get('user_id') is None:
        return redirect('/')
    
    show = Show.get_by_id(id)

    return render_template('edit.html', show=show)


@app.route('/shows/edit/process', methods=['POST'])
def update_show():
    if session.get('user_id') is None:
        return redirect('/')
    
    if not Show.validate_show(request.form):
        return redirect(f'/shows/edit/{request.form["id"]}')
    
    Show.update_show_info(request.form)

    return redirect('/shows')


@app.route('/shows/delete/<int:id>')
def delete_show(id):
    if session.get('user_id') is None:
        return redirect('/')

    Show.delete_show(id)
    return redirect('/shows')
