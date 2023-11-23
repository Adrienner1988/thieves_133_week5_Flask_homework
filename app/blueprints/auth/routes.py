from app.blueprints.auth import auth
from .forms import LoginForm, SignUpForm
from flask import request, flash, redirect, url_for, render_template
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

#log in
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Welcome, {queried_user.full_name} you are logged in!', 'primary')
            return redirect(url_for('main.home'))
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)
    

#log out
@auth.route('/logout')
@login_required
def logout():
    flash(f'You have been successfully logged out!','primary') 
    logout_user()
    return redirect(url_for('auth.login'))


#sign up  
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        password = form.password.data

        #Create an instance for user class
        user = User(full_name, email, password)

        # add user to database
        db.session.add(user)
        db.session.commit()

        flash(f'Thank you {full_name} for becoming a member of the Pokédex!', 'warning')
        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html', form=form)
    

    