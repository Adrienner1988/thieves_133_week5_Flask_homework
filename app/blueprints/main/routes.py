from app.blueprints.main import main
from flask import render_template, request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user, login_required
import requests
from .forms import SearchForm, CatchForm
from app.models import db, Poke, User



#home
@main.route('/')
@main.route('/home')
@login_required
def home():
    return render_template('home.html')


# search pokemon/pull data
@main.route('/search', methods=['GET', 'POST'])
@login_required
def pokemon_search():
    form = SearchForm()
    form = CatchForm()
    if request.method == 'POST' and form.validate_on_submit():
        pdata = form.search.data.lower()
        pokemon = ''
        if pdata.isdigit():
            pokemon = Poke.query.filter(Poke.id==pdata)
        pokemon = Poke.query.filter(Poke.name==pdata).first()
        print(pokemon, 'line 26')
        if pokemon:
            return render_template('search.html', pokemon=pokemon, form=form)
        else:
            url = f'https://pokeapi.co/api/v2/pokemon/{pdata}'
            response = requests.get(url)
            more_data = response.json()
            pokemon_dict = {
                'id': more_data['id'],
                'name': more_data['name'],
                'ability': more_data['abilities'][0]['ability']['name'],
                'base_experience': more_data['base_experience'],
                'attack_stat': more_data['stats'][1]['base_stat'],
                'hp_stat': more_data['stats'][0]['base_stat'],
                'defense_stat': more_data['stats'][2]['base_stat'],
                'sprite': more_data['sprites']['front_shiny']
                }
            print(pokemon_dict)
            pokemon = Poke(
                    id=pokemon_dict['id'],
                    name=pokemon_dict['name'],
                    ability=pokemon_dict['ability'],
                    attack_stat=pokemon_dict['attack_stat'],
                    hp_stat=pokemon_dict['hp_stat'],
                    defense_stat=pokemon_dict['defense_stat'],
                    sprite=pokemon_dict['sprite'],
                    poke_added = any  
                )
            db.session.add(pokemon)
            db.session.commit()
            flash(f'Would you like to add {pokemon.name} to your team? Hit the catch button below!', 'warning')
            return render_template('search.html', pokemon=pokemon, form=form)
      
    return render_template('search.html', form=form)
    
            
            

       
                
               
        
    
        
        


   

       




   