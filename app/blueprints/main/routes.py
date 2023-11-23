from app.blueprints.main import main
from flask import render_template, request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user, login_required
import requests
from .forms import SearchForm
from app.models import db, Poke, User, user_poke



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
        #taking in information from form to search
        pdata = form.search.data
        pokemon = ''
        #checking to see if this information is in the database
        if pdata.isdigit():
            pokemon = Poke.query.filter(Poke.id==int(pdata)).first()
        else:
            pokemon = Poke.query.filter(Poke.name==pdata.lower()).first()
        print(pokemon, 'line 26')
        #if information is in the data base add to the database ans return to the user 
        if pokemon:
            return render_template('search.html', pokemon=pokemon, form=form)
        #else create the pokemon and add the the database
        else:
            print(pdata)
            url = f'https://pokeapi.co/api/v2/pokemon/{pdata.lower()}'
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
                )
            #add then commit the pokemon to the database
            db.session.add(pokemon)
            db.session.commit()
            #flash message and return back to the search page
            flash(f'Would you like to add {pokemon.name} to your team? Hit the catch button below!', 'warning')
            return render_template('search.html', form=form, pokemon=pokemon)
      
    return render_template('search.html', form=form)
    

#catching      
# @main.route('/catch/<int:poke_id>')
# def catch(poke_id):
#     poke = Poke.query.get(poke_id)
#     print(poke)
#     current_user.Pokemon.append(poke)
#     db.session.commit()
#     return redirect(url_for('main.pokemon_search'))

 
@main.route('/catch/<int:poke_id>')
@login_required
def catch(poke_id):
    poke = Poke.query.get(poke_id)
    # seeing if user has the pokemon in their team already
    if poke in current_user.Pokemon:
        flash(f'{poke_id} is already in your team, pick another Pokémon.', 'warning')
        return redirect(url_for('main.pokemon_search'))
    
    # seeing if the team has 6 pokemon
    if len(current_user.Pokemon) >= 6:
        flash(f'Your team is full, release another Pokémon to catch this one.', 'danger')
        return redirect(url_for('main.pokemon_search'))
    
    #if the if checks pass adding the pokemon to team
    current_user.Pokemon.append(poke)
    db.session.commit()
    flash(f'{poke_id} has been added to your team!', 'success')
    print(poke)
    return redirect(url_for('main.pokemon_search'))
              
               
# releasing a Pokemon
@main.route('/release/<int:poke_id>')
@login_required
def release(poke_id):
    print(poke_id)
    #getting the poke from the database
    poke = Poke.query.get(poke_id)
    if poke and current_user.Pokemon:
    #deleting from the database
        db.session.delete(poke)
        db.session.commit()
        flash(f'{poke_id} has been released from your team!', 'success')
        return redirect(url_for('main.team'))

        
#Seeing the team
#querying objects from the database from the Poke table, creating an object (my_team),then passing the pokemon, looping and showing the pokemon on the front end
@main.route('/team')
@login_required
def team():
    my_team = Poke.query.all()
    return render_template('team.html', my_team=my_team)




   

       




   