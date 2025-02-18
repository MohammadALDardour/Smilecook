from flask import Flask
from flask_restful import Api

from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource


app = Flask(__name__)
api = Api(app)
# http POST localhost:5000/recipes name="one" description="description" num_of_servings:=3 cook_time:=5 directions="dire"
# 77
api.add_resource(RecipeListResource, '/recipes')
api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')
api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')


if __name__ == '__main__':
    app.run(port=5000, debug=True)