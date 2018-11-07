import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'online_cookbook'
app.config["MONGO_URI"] = 'mongodb://admin:lightbulb10@ds151523.mlab.com:51523/online_cookbook'

mongo = PyMongo(app)

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
    _cuisines = mongo.db.cuisines.find()
    cuisine_list = [cuisine for cuisine in _cuisines]
    return render_template("addrecipe.html", cuisines=cuisine_list)


@app.route('/insert_recipe/', methods=['GET','POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    dictionary = recipes.insert_one(request.form.to_dict())
    print(dictionary)
    return redirect(url_for("get_recipes"))
    

if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
