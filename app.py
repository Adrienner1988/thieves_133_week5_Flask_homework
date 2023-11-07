from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/home')
def hello_trainers():
    return "<h1>Hello Pokémon Trainers!</h1>"

# @app.route('/user/<username>')
# def show_user(username):
#     return f'Welcome {username}!'

@app.route('/search', methods=['GET', 'POST'])
def pokemon_search():
    if request.method == 'POST':
        data = request.form.get('data').lower()
        print(data)
        try:
            url = f'https://pokeapi.co/api/v2/pokemon/{data}'
            response = requests.get(url)
            more_data = response.json()
            get_poke = get_pokemon_data(more_data)
            return render_template('search.html', data=get_poke)
        except: 
            return render_template('search.html')
    else:
         return render_template('search.html')
        
def get_pokemon_data(data):
        pokemon_dict = {
                'name': data['forms'][0]['name'],
                'ability': data['abilities'][0]['ability']['name'],
                'base_experience': data['base_experience'],
                'sprite': data['sprites']['front_shiny'],
                'attack_stat': data['stats'][1]['base_stat'],
                'hp_stat': data['stats'][0]['base_stat'],
                'defense_stat': data['stats'][2]['base_stat']
            }
        return pokemon_dict

     
        




    
    
      

        
# def get_pokemon_data(data):
        # new_pokemon_data = []
        # for pokemon in data: