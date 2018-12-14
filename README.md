# Live To Cook

The project is a database-driven online cookbook. The project utilises Flask to
create the application, using MongoDB as a data store, with the bulk of the
back-end functionality written in python.

The project includes each function of CRUD, allowing a user to create, read,
update and delete recipes that are upheld by persistent storage.

## UX Design

My design was inspired by Pinterest and Tumblr, where images make up the
majority of the page as opposed to text. This creates a user-friendly, more
interesting web-page that a user will want to interact with. I believe this is
preferable for a cookbook where a user would be likely to choose a recipe they
like the look of instead of 'like the sound of' (with text).

The homepage allows a user to hover over an image to find out more information
about the recipe before clicking and finding ingredients/preparation
instructions.

Within the recipe's information page the page is structured with defined
sections. A shopping list style for the list of ingredients and a large section
for the instructions.

In terms of adding a recipe the form is clear. It allows a user to add/ remove
ingredients and preparation steps with the use of a simple button (JavaScript).
The form makes use of WTForms for validation and security which provides good
feedback to the user.

The Filter modal offers a user the ability to narrow down the recipes on the 
website dependent on the user's requirements. I chose a modal to reduce the 
clutter within the navigation bar, trying to keep the design as minimalist
as possible. 

To return to the home-page a user simply clicks the Logo (a common convention),
I also added a home button alongside the logo to make this clearer.

## Features

#### Add Recipe

A user is able to fill out a form and add a recipe to the database and therefore
the site using MongoDBs insert-one() function.

The upvotes section is not seen on the form, a JavaScript function is used to
produce a number between 0-10000 and applied to the recipe. This is to show how
the functionality would work with a live website.

#### Edit Recipe

A user is able to make edits to recipes found on the website. MongoDB allocates
each entry into a collection with an object ID and this is what is used to 
locate the individual recipe the user wants to edit and pre-fill the form
for the user. After the user has made the necessary changes they submit the form
and MongoDB's update() method to update the recipe.

#### Find Recipe

Once a user selects a recipe from the home-page the MongoDB find() method uses
the object ID to find the requested recipe. The user is then taken through 
to the recipe's page where information from the database is presented in a 
readable format to the user.

#### Delete Recipe

Each recipe has a 'Delete Recipe' button found at the bottom of the page. Once
clicked it uses the remove() mongoDB method.

#### Manage Cuisines

Each recipe has a cuisine, and the user is able to add, edit or delete cuisines
found on the website. This is an entirely different collection that has a
relationship with the recipes collection.

#### Filter Recipes

This functionality allows a user to narrow down the recipes and tailor the
filter to their personal preferences. The user is able to filter by cuisine,
time to cook, cooking difficulty or sort the recipes by upvotes. This feature
queries the database for each different parameter and returns a list only
including the requested parameter. The sort by number of upvotes uses the 
sort() method to sort by the upvotes field.

## Technologies Used

- Python 3.4.3
- Flask (Python Microframework)
- BootStrap 3
- Google Fonts
- JavaScript
- CSS
- HTML
- WTForms
- Materialize

## Testing

#### Testing Add Recipe Form

- Test that a new added recipe immediately appears on the website's homepage
- Go to form and try to submit empty fields and make sure WTForms 
InputRequired() is working
- Try to submit an empty ingredients list and make sure in-line validation is
working
- Try to submit a value in the Image URL field that is not a valid URL to make
sure the custom JavaScript validator is working
- Ensure that the random number JS function for upvotes is being created when 
adding new recipe.
- Ensure the adding of new ingredients and steps rows through JavaScript is
working and that they are creating the correct names within the documents 
in MongoDB.
- Making sure that the select fields are being populated with all of the 
correct choices
- Ensure that the removal of newly created rows for ingredients/preparation
steps is possible and make sure that all of the rows are unable to be deleted
with feedback for user if they try.

#### Testing Edit Recipe Form

- Make sure that the form is being populated with the correct data from the
MongoDB document when editing recipe.
- Ensure that adding/removing ingredient/preparation step rows is not causing
an issue with clashing names when submitted
- Ensure a recipe is able to be updated more than once without any bugs
occuring (such as fields going missing or name clashes causing issues)
- Test that the select fields are producing the correct options.

#### Other Tests

- Make sure the 'delete recipe' functionality is removing the correct document.
- Ensure that newly added cuisines become available on the add recipe form.
- Make sure removing a cuisine that recipes have as their cuisine doesn't cause
the website to crash.

## Database Schema

The database is structured with two collections, recipes and cuisines. The two
collections are related as recipes contains a 'cuisine name' key that
corresponds the cuisine documents.

The recipes document itself contains unstuctured data. With key/value pairs
that make up a description of the recipe. The ingredient name, quantity and
value all have the same number within the key, and they are grouped through the
use of sorting by number and sliced for data representation.

An example of a recipe document can be found in static/images/doc_example.png


## Deployment

To Clone the project from github:

```python
$ git clone https://github.com/jstokes1994/online-cookbook.git
```

I recommend deploying the project in a virtual envioronment:

```python
$ cd directory-name
$ python3 -m venv virtual-env-name
```

You will need to install the dependencies found in the requirements.txt file:

```python
$ pip3 install -r requirements.txt 
```

To run the project locally use:

```python
$ python3 run.py
```

You can also run the app through Heroku.

The project was deployed to Heroku with config vars:

- IP = 0.0.0.0
- PORT = 5000

https://online-cookbook-js.herokuapp.com/

There are no differences between the development and deployed versions.

Note the project is written with Python3 and not Python2.

