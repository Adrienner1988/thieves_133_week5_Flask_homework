from flask import request, render_template
import requests
from app import app
from app.forms import LoginForm, SearchForm, SignUpForm 


@app.route('/')
def hello_trainers():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        return 'You have successfully logged in!'
    else:
        return render_template('login.html', form=form)
    
@app.route('.singup', methods=['GET', ['POST']])
def signUp():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        return f'{full_name} Thank you for becoming an official member of the Pokédex!'
    else:
        return render_template('signup.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def pokemon_search():
    form = SearchForm()
    if request.method == 'POST':
        form = form.search.data
        try:
            url = f'https://pokeapi.co/api/v2/pokemon/{data}'
            response = requests.get(url)
            more_data = response.json()
            pokemon_dict = {
                'name': data['forms'][0]['name'],
                'ability': data['abilities'][0]['ability']['name'],
                'base_experience': data['base_experience'],
                'attack_stat': data['stats'][1]['base_stat'],
                'hp_stat': data['stats'][0]['base_stat'],
                'defense_stat': data['stats'][2]['base_stat'],
                'sprite': data['sprites']['front_shiny']
            }
            return render_template('search.html', data=pokemon_dict, form=form)
        except: 
            return render_template('search.html', form=form)
    else:
        return render_template('search.html', form=form)

     