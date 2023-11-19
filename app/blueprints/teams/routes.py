from app.blueprints.teams import teams
from flask import request, render_template, request, flash, redirect, url_for, render_template
from flask_login import login_required, login_required, current_user
import requests
from app.models import Poke, User, db, user_poke



# team 
@teams.route('/team', methods=['POST'])
@login_required
def poke_team():
   player = User.query.get(current_user.id)
   if player:
       all_players = player.caught.all()
       return render_template('team.html', all_players=all_players)
#    else:
#     return 'Player not found.'



# releasing a Pokemon
@teams.route('/release/<int:poke_id>', methods=['POST'])
@login_required
def release_poke(poke_id):
    poke = Poke.query.get(poke_id)
    
    if poke in current_user.id == user_poke.id:
        db.session.delete(poke)
        db.session.commit()
    else:
        flash(f'{poke_id} has been removed from your team.')
        return  redirect(url_for('team.html'))
    

    
    
# # catching a Pokemon
# @team.route('/catch/<int:poke_id>')
# @login_required
# def catch_poke(poke_id):
#     print(poke_id)
#     poke = Poke.query.get(poke_id)
#     if poke and poke.poke_id == current_user.id:
#         #setting queried post to those of the instance
#             poke.name = Poke.name.data
#             poke.ability = Poke.ability.data
#             poke.attack_stat = Poke.attack_stat.data
#             poke.hp_stat = Poke.hp_stat.data
#             poke.defense_stat = Poke.defense_stat.data
#             poke.sprite = Poke.sprite.data
#             poke.user_id = Poke.current_user.id

#             #add to database
#             db.session.add(poke)
#             db.session.commit()

#             flash(f'{poke.name} has been added to your team!')
#             return redirect(url_for('team.html'))
#     else:
#             flash(f'Your team is full, please release to add {poke.name}')
#             return redirect(url_for('main.pokemon_search'))




@teams.route('/search', methods=['GET', 'POST'])
@login_required
def pokemon_search():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        pdata = form.search.data.lower()
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
