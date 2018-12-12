import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from wtforms import StringField, IntegerField, SelectField, SubmitField, FileField
from wtforms.validators import InputRequired, URL, ValidationError
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'online_cookbook'
app.config["MONGO_URI"] = 'mongodb://admin:lightbulb10@ds151523.mlab.com:51523/online_cookbook'
app.config["SECRET_KEY"] = 'thisisasecret'


mongo = PyMongo(app)


# WTForms configuration
def is_valid_url(form, field):
    if "www." not in field.data:
        raise ValidationError('Must contain a valid URL')


class AddRecipe(FlaskForm):
    recipe_name = StringField('Recipe Name', validators=[InputRequired()])
    recipe_author = StringField('Recipe Author', validators=[InputRequired()])
    image_url = StringField("Image URL for the recipe - <a href='https://www.quora.com/How-do-I-make-a-URL-for-my-image'> How to create URL for local image</a>",
                            validators=[URL()])
    serves = StringField('Serves', validators=[InputRequired()])
    cuisine_name = SelectField('Cuisine:', validators=[InputRequired()])
    difficulty = SelectField('How difficult is this recipe?', choices=
                             [('easy', 'Easy'),('medium', 'Medium'),
                              ('hard', 'Hard')],
                               validators=[InputRequired()])
    cooking_time = SelectField('What category of cooking time is the recipe?',
                                choices=[('0-30', '0-30 minutes'), ('30-60',
                                '30-60 minutes'), ('60-90', '60-90 minutes'),
                                ('90+', '90+ minutes')],
                                 validators=[InputRequired()])
    total_time = IntegerField('How long will it take to cook in minutes?',
                                  validators=[InputRequired()])
    addrow = SubmitField('Add Row')

class AddCuisineForm(FlaskForm):
    cuisine_name = StringField('Cuisine Name', validators=[InputRequired()])


@app.route('/')
@app.route('/get_recipes/')
def get_recipes():
    """
    App homepage which displays images of the different recipes on the website
    """
    all_recipes = mongo.db.recipes.find()
    return render_template("recipes.html", recipes=all_recipes)
# Uses the find() function to return all of the recipes from the Mongo Collection


@app.route('/show_recipe/<recipe_id>/')
def show_recipe(recipe_id):
    """
    The view that displays recipe information based on the recipe ID.
    Produces a list of results as key, value pairs using items() method.
    Then filters the results for ingredients/steps and creates another list
    The list is sorted - for ingredients it keeps the name/unit/quantity
    together.
    The next step puts the ingredients/steps into independent lists to be
    iterated through and displayed on the HTML page.
    """
    
    recipe_id = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    list_of_results = recipe_id.items()
    
    filter_for = ''.join(['ingredients_'])
    filter_list = [tup for tup 
                   in list_of_results if filter_for in ''.join(str(tup))]
    sorted_list = sorted(filter_list, key=lambda x: x[0])
    counter = 0
    a = 0
    b = 3
    ingredient_list = []
    
    while counter < len(sorted_list)/3:
        ingredient_list.append(sorted_list[slice(a,b)])
        a += 3
        b += 3
        counter += 1
        
    filter_for_2 = ''.join(['steps_'])
    filter_list_2 = [tup for tup in 
                     list_of_results if filter_for_2 in ''.join(str(tup))]
    sorted_list_2 = sorted(filter_list_2, key=lambda x: x[0])
    counter_2 = 0
    x = 0
    y = 1
    steps_list = []
    
    while counter_2 < len(sorted_list_2):
        steps_list.append(sorted_list_2[slice(x,y)])
        x += 1
        y +=1
        counter_2 += 1
        
    return render_template("show_recipe.html", recipe=recipe_id,
                            ingredients=ingredient_list, steps=steps_list, 
                            enumerate=enumerate)


@app.route('/add_recipe/', methods=['GET', 'POST'])
def add_recipe():
    """
    This is a page where a user can add a recipe. It makes use of WTForms which
    provides form validation and a CSRF token for security
    """
    form = AddRecipe(request.form)
    
    """
    Provides the select field within the form with choices using the find()
    method to search within the cuisines document.
    """
    form.cuisine_name.choices = [(cuisine['name'], cuisine['name'].capitalize())
                                 for cuisine in mongo.db.cuisines.find()]
    return render_template("addrecipe.html", form=form)


@app.route('/insert_recipe/', methods=['GET','POST'])
def insert_recipe():
    """
    This function is called when a user clicks the submit button on the add
    recipe form. Uses the insert_one() method to add to the recipes document.
    """
    recipes = mongo.db.recipes
    dictionary = recipes.insert_one(request.form.to_dict())
    return redirect(url_for("get_recipes"))
    

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    """
    This function removes the recipe from the document using the remove() 
    method when the 'delete recipe' button is pressed
    """
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))
    

@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """
    This view allows the user to make changes to recipes.
    It uses the recipe_id to fill the form with the values already chosen in the
    original creation of the recipe.
    Uses the same method as add_recipe() to collate the ingredients and steps 
    into independent lists. On submit, the update function is called.
    
    """
    form = AddRecipe(request.form)
    form.cuisine_name.choices = [(cuisine['name'], cuisine['name'].capitalize())
                                 for cuisine in mongo.db.cuisines.find()]
    
    recipe_id = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    list_of_results = recipe_id.items()
    
    filter_for = ''.join(['ingredients_'])
    filter_list = [tup for tup in list_of_results if filter_for
                   in ''.join(str(tup))]
    sorted_list = sorted(filter_list, key=lambda x: x[0])
    counter = 0
    a = 0
    b = 3
    ingredient_list = []
    no_of_ingredients = len(sorted_list)/3
    while counter < no_of_ingredients:
        ingredient_list.append(sorted_list[slice(a,b)])
        a += 3
        b += 3
        counter += 1
        
    filter_for_2 = ''.join(['steps_'])
    filter_list_2 = [tup for tup in list_of_results if filter_for_2 
                     in ''.join(str(tup))]
    sorted_list_2 = sorted(filter_list_2, key=lambda x: x[0])
    counter_2 = 0
    x = 0
    y = 1
    steps_list = []
    
    while counter_2 < len(sorted_list_2):
        steps_list.append(sorted_list_2[slice(x,y)])
        x += 1
        y +=1
        counter_2 += 1
        
    numbers = list(range(1, 100, 1))
    
    zipped_list = list(zip(ingredient_list, numbers))
    
    zipped_list2 = list(zip(steps_list, numbers))
    
    return render_template("edit_recipe.html", form=form,
    recipe=recipe_id, ingredients=zipped_list,
    zipped_list2=zipped_list2)
    

@app.route('/update_recipe/<recipe_id>', methods=['GET', 'POST'])
def update_recipe(recipe_id):
    """
    This view takes the data input from the user from the edit_recipe form and
    uses the MongoDB update() method to update changes to the recipe.
    The user is then redirected to the recipe's page.
    """
    form = AddRecipe(request.form)
    mongo.db.recipes.update({'_id': ObjectId(recipe_id)}, 
                            request.form.to_dict())
    
    return redirect(url_for('show_recipe', recipe_id=recipe_id))


@app.route('/find_recipe/<cuisine_name>', methods=['GET', 'POST'])
def find_recipe_by_cuisine(cuisine_name):
    """
    This view filters the recipes by cuisine name (found within recipe document)
    The function searches each recipe for the particular cuisine_name and
    returns the recipes that match.
    It also returns a count of the recipes found as feedback to the user.
    The recipes are returned in order of upvotes.
    """
    db_query = { 'cuisine_name': cuisine_name }
    recipe_by_cuisine = mongo.db.recipes.find(db_query).sort([("upvotes", -1)])
    results_total = mongo.db.recipes.count(db_query)
    return render_template("recipe_by_cuisine.html", recipes=recipe_by_cuisine,
                           results_total=results_total)
                           

@app.route('/search_recipe/<difficulty>', methods=['GET', 'POST'])
def search_recipe_by_difficulty(difficulty):
    db_query = { 'difficulty': difficulty }
    recipe_by_difficulty = mongo.db.recipes.find(db_query).sort([("upvotes", -1)])
    results_total = mongo.db.recipes.count(db_query)
    return render_template("recipe_by_difficulty.html", 
                           recipes=recipe_by_difficulty, 
                            results_total=results_total)
                            

@app.route('/look_for_recipe/<cooking_time>', methods=['GET', 'POST'])
def search_recipe_by_time(cooking_time):
    db_query = { 'cooking_time': cooking_time }
    recipe_by_time = mongo.db.recipes.find(db_query).sort([("upvotes", -1)])
    results_total = mongo.db.recipes.count(db_query)
    return render_template("recipe_by_time.html", 
                           recipes=recipe_by_time, 
                            results_total=results_total)
                            

@app.route('/sort_recipes_by_upvotes', methods=['GET', 'POST'])
def sort_recipes_by_upvotes():
    recipes_by_upvotes = mongo.db.recipes.find().sort([("upvotes", -1)])
    results_total = mongo.db.recipes.count()
    return render_template("recipes_by_upvotes.html",
                           recipes=recipes_by_upvotes,
                            results_total=results_total)
    

@app.route('/get_cuisines/')
def get_cuisines():
    """
    This view finds and returns all of the documents found within the cuisines
    collection.
    """
    return render_template("cuisines.html", cuisines=mongo.db.cuisines.find())


@app.route('/new_cuisine/', methods=['GET', 'POST'])
def new_cuisine():
    """
    Uses a very simple WTForm to allow a user to add a new cuisine
    """
    form = AddCuisineForm()
    return render_template("addcuisine.html", form=form)
    

@app.route('/insert_cuisine/', methods=['GET', 'POST'])
def insert_cuisine():
    """
    When user submits the new cuisine form this view will run and redirect 
    to the homepage.
    The function takes the input data from the form and structures it as a
    key/value pair before inserting to the cuisines collection using
    insert_one()
    """
    cuisines = mongo.db.cuisines
    cuisine_doc = {'name': request.form.get('cuisine_name')}
    cuisines.insert_one(cuisine_doc)
    return redirect(url_for('get_cuisines'))


@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
    """
    Simply removes the cuisine (based on cuisine ID) from the cuisines 
    collection when the 'delete cuisine' button is clicked.
    """
    mongo.db.cuisines.remove({'_id': ObjectId(cuisine_id)})
    return redirect(url_for("get_cuisines"))

   
@app.route('/edit_cuisine/<cuisine_id>')
def edit_cuisine(cuisine_id):
    """
    This allows the user to edit the name of the cuisine again using WTForms
    It uses the cuisine_id to find the correct document within the cuisines
    collection.
    """
    form = AddCuisineForm()
    return render_template("editcuisine.html", form=form,
    cuisine=mongo.db.cuisines.find_one({'_id': ObjectId(cuisine_id)}))


@app.route('/update_cuisine/<cuisine_id>', methods=['GET', 'POST'])
def update_cuisine(cuisine_id):
    """
    This view is invoked when the user submits the edit_cuisine form.
    The update() method is used, repeating the original cuisine_id and then
    inserting the form data for the name of the cuisine.
    """
    mongo.db.cuisines.update(
        {'_id': ObjectId(cuisine_id)},
        {'name': request.form.get('cuisine_name')})
    return redirect(url_for("get_cuisines"))


@app.context_processor
def inject_cuisines():
    """
    This is used so that the cuisines can be used within base.html, in the nav
    bar. As base.html does not use app.route, this allows the cuisines to be
    passed to the template.
    """
    all_cuisines = mongo.db.cuisines.find()
    return dict(all_cuisines=all_cuisines)
    

@app.route('/form/', methods=['GET', 'POST'])
def test_form():
    return render_template('form.html')
    


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
