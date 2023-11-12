from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from app.forms import LoginForm, SearchForm, SignUpForm
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

#home
@app.route('/')
def home():
    return render_template('home.html')

#log in
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Hello, {queried_user.full_name} you have successfully logged in!', 'primary')
            return redirect(url_for('home'))
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)
    

#log out
@app.route('/logout')
@login_required
def logout():
    flash(f'You have been successfully logged out!','danger') 
    logout_user()
    return redirect(url_for('login'))

#sign up  
@app.route('/signup', methods=['GET', 'POST'])
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
        return redirect(url_for('home'))
    else:
        return render_template('signup.html', form=form)
    
# search pokemon/pull data
@app.route('/search', methods=['GET', 'POST'])
def pokemon_search():
    print('enroute')
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        print('POST')
        pdata = form.search.data.lower()
        print(pdata)
        try:
            url = f'https://pokeapi.co/api/v2/pokemon/{pdata}'
            response = requests.get(url)
            more_data = response.json()
            pokemon_dict = {
                'name': more_data['forms'][0]['name'],
                'ability': more_data['abilities'][0]['ability']['name'],
                'base_experience': more_data['base_experience'],
                'attack_stat': more_data['stats'][1]['base_stat'],
                'hp_stat': more_data['stats'][0]['base_stat'],
                'defense_stat': more_data['stats'][2]['base_stat'],
                'sprite': more_data['sprites']['front_shiny']
            }
            print(pokemon_dict)
            return render_template('search.html', pdata=pokemon_dict, form=form)
        except: 
            return render_template('search.html', form=form)
    else:
        return render_template('search.html', form=form)

     