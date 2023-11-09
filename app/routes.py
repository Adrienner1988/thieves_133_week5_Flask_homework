from flask import request, render_template
import requests
from app import app
from app.forms import LoginForm, SearchForm


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
    

@app.route('/search', methods=['GET', 'POST'])
def pokemon_search():
    form = SearchForm()
    if request.method == 'POST':
        data = request.form.get('data')
        try:
            url = f'https://pokeapi.co/api/v2/pokemon/{data}'
            response = requests.get(url)
            more_data = response.json()
            get_poke = get_pokemon_data(more_data)
            return render_template('search.html', data=get_poke)
        except: 
            return render_template('search.html', form=form )
    else:
         return render_template('search.html', form=form)
        

def get_pokemon_data(data):
        pokemon_dict = {
                'name': data['forms'][0]['name'],
                'ability': data['abilities'][0]['ability']['name'],
                'base_experience': data['base_experience'],
                'attack_stat': data['stats'][1]['base_stat'],
                'hp_stat': data['stats'][0]['base_stat'],
                'defense_stat': data['stats'][2]['base_stat'],
                'sprite': data['sprites']['front_shiny']
            }
        return pokemon_dict

     