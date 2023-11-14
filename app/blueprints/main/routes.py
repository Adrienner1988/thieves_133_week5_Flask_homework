from app.blueprints.main import main
from flask import render_template, request
from flask_login import login_required 
import requests
from .forms import SearchForm


#home
@main.route('/')
def home():
    return render_template('home.html')


# search pokemon/pull data
@main.route('/search', methods=['GET', 'POST'])
@login_required
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
