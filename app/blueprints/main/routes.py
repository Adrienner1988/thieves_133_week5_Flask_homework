from app.blueprints.main import main
from flask import render_template, request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user, login_required
import requests
from .forms import SearchForm
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
    if request.method == 'POST' and form.validate_on_submit():
        pdata = form.search.data.lower()
        pokemon = Poke.query.filter(name=pdata).first() #ask about dupes in the data base, how to prevent?
        if pokemon:
            print(pokemon)
            return render_template('search.html', info=pokemon, form=form)
        else:
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
            poke = Poke(
                    name=pokemon_dict['name'],
                    ability=pokemon_dict['ability'],
                    attack_stat=pokemon_dict['attack_stat'],
                    hp_stat=pokemon_dict['hp_stat'],
                    defense_stat=pokemon_dict['defense_stat'],
                    sprite=pokemon_dict['sprite'],
                    poke_added = any  
                )
            db.session.add(poke)
            db.session.commit()
            flash(f'{poke.name} has been added to your team!', 'warning')
            return render_template('search.html', poke=poke, form=form)
      
    return render_template('search.html', form=form)
    
            
            

       
                
               
        
    
        
        


   

       




   