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
    
    
@app.route('/signup', methods=['GET', 'POST'])
def join():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        return f'Thank you for becoming an official member of the Pokédex!'
    else:
        return render_template('signup.html', form=form)


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

     