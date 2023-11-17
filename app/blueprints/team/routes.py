from app.blueprints.team import team
from app.models import Poke, db
from flask import request, flash, redirect, url_for, render_template
from .forms import TeamForm
from app.models import Poke, db
from flask_login import current_user, login_required


# team page
@team.route('/create',  methods=['GET', 'POST'])
@login_required
def create():
    form = TeamForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        ability = form.ability.data
        attack_stat = form.attack_stat.data
        hp_stat = form.hp_stat.data
        defense_stat = form.defense_stat.data
        sprite = form.sprite.data
        user_id = current_user.id
    # print(TeamForm)

        # creating an instance of Poke class in models
        poke = Poke(name, ability, attack_stat,hp_stat, defense_stat, sprite, user_id)
        print(poke)

        db.session.add(poke)
        db.session.commit()
        
        flash(f'{name} has been added to your team!', 'danger')
        return redirect(url_for('team.create'))
    else:
        render_template('create_team.html', form=form)


# read the addition to team
# @team.route('/myteam')
# @login_required
# def team():
#     my_pokemon = Poke.query.all()
#     return render_template('team.html', my_pokemon=my_pokemon)


# # catch pokemon
# @team.route('/catch/<int:name>', methods=['POST'])
# @login_required
# def catch_poke():
#     pass

# #remove pokemon
# @team.route('/release')
# @login_required
# def release_poke():
#     pass