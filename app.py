import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from wtforms import Form, BooleanField, StringField, validators, PasswordField, TextField, IntegerField, FieldList, FormField, TextAreaField, SelectField
from wtforms.validators import InputRequired, DataRequired
from flask_wtf import FlaskForm
from wtforms_dynamic_fields import WTFormsDynamicFields

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'online_cookbook'
app.config["MONGO_URI"] = 'mongodb://admin:lightbulb10@ds151523.mlab.com:51523/online_cookbook'
app.config["SECRET_KEY"] = 'thisisasecret'

mongo = PyMongo(app)


class Ingredients(FlaskForm):
    ingredient_name = TextField('Ingredient Name', [validators.required()])
    ingredient_quantity = TextField('Quantity', [validators.required()])
    ingredient_unit = TextField('Unit', [validators.required()])

class RecipeMethod(FlaskForm):
    steps = TextAreaField('Step:', [validators.required()])

class AddRecipe(FlaskForm):
    recipe_name = StringField('Recipe Name', validators=[InputRequired()])
    ingredients = FieldList(FormField(Ingredients), min_entries=1)
    steps = FieldList(FormField(RecipeMethod), min_entries=1)
    recipe_author = StringField('Recipe Author', validators=[InputRequired()])
    image_url = StringField('Image URL', validators=[DataRequired()])
    serves = StringField('Serves', validators=[InputRequired()])
    cuisine_type = SelectField('Cuisine:', validators=[InputRequired()])

class TelephoneNumber(FlaskForm):
    country_code = IntegerField('Country Code', [validators.required()])
    area_code = IntegerField('Area Code/Exchange', [validators.required()])
    number = TextField('Number')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    telephone_number = FieldList(FormField(TelephoneNumber), min_entries=2)
    gender = SelectField('Gender:')

class AddCuisineForm(FlaskForm):
    cuisine_name = StringField('Cuisine Name', validators=[InputRequired()])
    

@app.route('/form/', methods=['GET', 'POST'])
def form():
    form = LoginForm()
    form.gender.choices = [(cuisine['_id'], cuisine['name']) for cuisine in mongo.db.cuisines.find()]
    if form.validate_on_submit():
        return '<h1>Thanks</h1>'
    return render_template("form.html", form=form)


@app.route('/')
@app.route('/get_recipes/')
def get_recipes():
    all_recipes = mongo.db.recipes.find()
    return render_template("recipes.html", recipes=all_recipes)
#Use the find() function to return all of the recipes from the Mongo Collection


@app.route('/show_recipe/<recipe_id>/')
def show_recipe(recipe_id):
    recipe_id = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("show_recipe.html", recipe=recipe_id)


@app.route('/add_recipe/', methods=['GET', 'POST'])
def add_recipe():
    form = AddRecipe()
    form.cuisine_type.choices = [(cuisine['_id'], cuisine['name'].capitalize()) for cuisine in mongo.db.cuisines.find()]
    return render_template("addrecipe.html", form=form)


@app.route('/insert_recipe/', methods=['GET','POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    dictionary = recipes.insert_one(request.form.to_dict())
    return redirect(url_for("get_recipes"))
    

@app.route('/find_recipe/<cuisine_name>', methods=['GET', 'POST'])
def find_recipe_by_cuisine(cuisine_name):
    db_query = { 'cuisine_name': cuisine_name }
    recipe_by_cuisine = mongo.db.recipes.find(db_query)
    results_total = mongo.db.recipes.count(db_query)
    return render_template("recipe_by_cuisine.html", recipes=recipe_by_cuisine,
                           results_total=results_total)
    

@app.route('/get_cuisines/')
def get_cuisines():
    return render_template("cuisines.html", cuisines=mongo.db.cuisines.find())


@app.route('/new_cuisine/', methods=['GET', 'POST'])
def new_cuisine():
    form = AddCuisineForm()
    return render_template("addcuisine.html", form=form)
    

@app.route('/insert_cuisine/', methods=['GET', 'POST'])
def insert_cuisine():
    cuisines = mongo.db.cuisines
    cuisine_doc = {'name': request.form.get('cuisine_name')}
    cuisines.insert_one(cuisine_doc)
    return redirect(url_for('get_cuisines'))


@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
    mongo.db.cuisines.remove({'_id': ObjectId(cuisine_id)})
    return redirect(url_for("get_cuisines"))

   
@app.route('/edit_cuisine/<cuisine_id>')
def edit_cuisine(cuisine_id):
    form = AddCuisineForm()
    return render_template("editcuisine.html", form=form,
    cuisine=mongo.db.cuisines.find_one({'_id': ObjectId(cuisine_id)}))


@app.route('/update_cuisine/<cuisine_id>', methods=['GET', 'POST'])
def update_cuisine(cuisine_id):
    mongo.db.cuisines.update(
        {'_id': ObjectId(cuisine_id)},
        {'name': request.form.get('cuisine_name')})
    return redirect(url_for("get_cuisines"))


@app.context_processor
def inject_cuisines():
    all_cuisines = mongo.db.cuisines.find()
    return dict(all_cuisines=all_cuisines)

if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
