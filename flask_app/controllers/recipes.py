from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.controllers import users
from flask_app.models.recipe import Recipe
from flask_app.models.user import User




@app.route('/dashboard')
def dashboard():
    user_data = {
        'id':  session['user_id']
    }
    user = User.get_one(user_data)
    recipes = Recipe.get_all_users_recipes()
    print(recipes)
    return render_template('dashboard.html', recipes = recipes, user = user)


#add new recipe page
@app.route('/create/recipe')
def add_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new_recipe.html')

#create recipe
@app.route('/submit/recipe', methods=['POST'])
def new_recipe():
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under30': int(request.form['under30']),
        'user_id' : session['user_id']
    }
    print(request.form)
    Recipe.save(data)
    return redirect('/dashboard')

#update recipe
@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/create/recipe')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under30': int(request.form['under30']),
        'id' : request.form['id']
    }
    Recipe.update(data)
    print(request.form)
    return redirect('/dashboard')

#show recipe info
@app.route('/recipe/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    recipe = Recipe.get_one(data)
    return render_template('show_recipe.html', user=User.get_one(user_data), recipe=recipe)

#edit recipe
@app.route('/edit/recipe/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template('edit_recipe.html', edit=Recipe.get_one(data), user=User.get_one(user_data))

#delete recipe
@app.route('/remove/recipe/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    Recipe.delete(data)
    return redirect('/dashboard')