from app.blueprints.main import main
from flask import render_template, request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user, login_required
import requests
from .forms import SearchForm
from app.models import db, Poke, User, user_poke



# home
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
        # taking in information from form to search
        pdata = form.search.data
    
        # checking to see if this information is in the database
        if pdata.isdigit():
            pokemon = Poke.query.filter(Poke.id==int(pdata)).first()
        else:
            pokemon = Poke.query.filter(Poke.name==pdata.lower()).first()
        print(pokemon, 'line 26')
        # if information is in the data base add to the database and return to the user 
        if pokemon:
            return render_template('search.html', pokemon=pokemon, form=form)
        # else create the pokemon and add the the database
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
            # add then commit the pokemon to the database
            db.session.add(pokemon)
            db.session.commit()
            # flash message and return back to the search page
            flash(f'Would you like to add {pokemon.name} to your team? Hit the catch button below!', 'warning')
            return render_template('search.html', form=form, pokemon=pokemon)
      
    return render_template('search.html', form=form)
 # what if the Pokemon does not exist? need error and redirect back to search 

#catching      
# @main.route('/catch/<int:poke_id>')
# def catch(poke_id):
#     poke = Poke.query.get(poke_id)
#     print(poke)
#     current_user.Pokemon.append(poke)
#     db.session.commit()
#     return redirect(url_for('main.pokemon_search'))

#catching a pokemon
@main.route('/catch/<int:poke_id>')
@login_required
def catch(poke_id):
    # querying from Poke table in database 
    poke = Poke.query.get(poke_id)
    print(poke)
    
    # seeing if current user has the pokemon on their team already
    if poke in current_user.Pokemon:
        flash(f'{poke_id} is already on your team, pick another Pokémon.', 'warning')
        return redirect(url_for('main.pokemon_search'))
    
    # seeing if the team has 5 pokemon
    if len(current_user.Pokemon) >= 5:
        flash(f'Your team is full, release another Pokémon to catch this one.', 'danger')
        return redirect(url_for('main.pokemon_search'))
    
    # if the if checks pass adding the pokemon to team
    current_user.Pokemon.append(poke)
    db.session.commit()
    print(poke)
    flash(f'{poke_id} has been added to your team!', 'success')
    return redirect(url_for('main.pokemon_search'))
              
               
# releasing a Pokemon
@main.route('/release/<int:poke_id>')
@login_required
def release(poke_id):
    # getting the poke from the Poke table in the database
    poke = Poke.query.get(poke_id)
    print(poke_id)

    if poke and current_user.Pokemon:
    # deleting from the user_poke table in database
        current_user.removefromteam(poke)
    flash(f'{poke_id} has been released from your team!', 'success')
    return redirect(url_for('main.team'))
    
        
# Seeing the team
# querying objects from the Pokemon relationship (in User table), creating an object (my_team),then passing the pokemon, looping and showing the pokemon on the front end
@main.route('/team')
@login_required
def team():
    my_team = current_user.Pokemon
    return render_template('team.html', my_team=my_team)


# trainers to battle
@main.route('/trainers')
@login_required
def trainers():
    # getting users from User table and displaying on team page
    all_trainers = User.query.all()
    return render_template('trainers.html', all_trainers=all_trainers)


# attack route to get to opponents page and see Pokemon
@main.route('/attack/<int:user_id>')
@login_required
def attack(user_id):
    user = User.query.get(user_id)
    print(user)
    op_team = user.Pokemon
    return render_template('op_team.html', user=user, op_team=op_team)


@main.route('/battle/<int:user_id>')
@login_required
def battle(user_id):
    #querying the users and their pokemon for battle depending on team size and redirecting if they are not full for battle
    offense_user = User.query.get(user_id)
    offense_pokemon= offense_user.Pokemon
    if len(offense_pokemon) < 5:
        flash("Opponent doesn't have enough Pokémon for a battle, pick another opponent.", 'danger')
        return redirect(url_for('main.trainers'))

    trainer = User.query.get(current_user.id)
    team = trainer.Pokemon

    if len(team) < 5:
        flash('You need five Pokémon for a battle.', 'warning')
        return redirect(url_for('main.pokemon_search'))
    
    return render_template('battle.html', offense_pokemon=offense_pokemon)


# battle results
@main.route('/results/<int:user_id>')
@login_required
def results(user_id):
    offense_user = User.query.get(user_id)
    print(user_id, 'line 175')
    offense_pokemon= offense_user.Pokemon

    trainer = User.query.get(current_user.id)
    print(current_user.id, 'line 179')
    team = trainer.Pokemon

    # Compare the attack_stat of the first Pokémon of each trainer
    winner = None

    if offense_pokemon.attack_stat > team.defense_stat:
        winner = trainer
      
    elif trainer.attack_stat > offense_pokemon.defense_stat:
        winner = offense_user
        print(winner, 'line 189')

    return redirect(url_for('main.results'), winner=winner)




   

       




   