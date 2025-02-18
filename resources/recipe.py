from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.recipe import Recipe, recipe_list


class RecipeListResource(Resource):
    def get(self):
        """
        Getting all the public recipes back. It does this by declaring a data list and getting all the recipes with is_publish=ture in recipe_list
        """
        data = []
        for recipe in recipe_list:
            if recipe.is_publish is True:
                data.append(recipe.data)
        return {'data': data}, HTTPStatus.OK


    def post(self):
        """
        It does get the JSON data back from the request using request.get_json and then creates the recipe object and stores that in recipe_list.
        Finally, it returns the recipe record with an HTTP Status code 201 CREATED. 
        """
        data = request.get_json()
        recipe = Recipe(
            name=data['name'],
            description=data['description'],
            num_of_servings=data['num_of_servings'],
            cook_time=data['cook_time'],
            directions=data['directions']
        )

        recipe_list.append(recipe)
        return recipe.data, HTTPStatus.CREATED
    

class RecipeResource(Resource):
    def get(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe_id == recipe_id and recipe.is_publish == True), None)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        return recipe.data, HTTPStatus.OK
    
    def put(self, recipe_id):
        data = request.get_json()
        recipe = next((recipe for recipe in recipe_list if recipe_id == recipe_id and recipe.is_publish == True), None)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus
        
        recipe.ane = data['name']
        recipe.description = data['description']
        recipe.num_of_servings = data['num_of_servings']
        recipe.cook_time = data['cook_time']
        recipe.directions = data['directions']

        return recipe.data, HTTPStatus.OK
    

    def delete(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id and recipe.is_publish == True))
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        recipe_list.remove(recipe)
        return {}, HTTPStatus.NO_CONTENT

class RecipePublishResource(Resource):
    def put(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        recipe.is_publish = True

        return {}, HTTPStatus.NO_CONTENT
    

    def delete(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe_id == recipe_id), None)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        recipe.is_publish = False
        return {}, HTTPStatus.NO_CONTENT
    