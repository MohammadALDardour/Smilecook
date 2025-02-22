from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus
from models.recipe import Recipe

class RecipeListResource(Resource):
    def get(self):
        """
        Getting all the public recipes back. It does this by declaring a data list and getting all the recipes with is_publish=ture in recipe_list
        """
        recipes = Recipe.get_all_published()

        data = []
        for recipe in recipes:
            if recipe.is_publish is True:
                data.append(recipe.data)
        return {'data': data}, HTTPStatus.OK

    @jwt_required
    def post(self):
        """
        It does get the JSON data back from the request using request.get_json and then creates the recipe object and stores that in recipe_list.
        Finally, it returns the recipe record with an HTTP Status code 201 CREATED. 
        """
        data = request.get_json()

        current_user = get_jwt_identity()

        recipe = Recipe(
            name=data['name'],
            description=data['description'],
            num_of_servings=data['num_of_servings'],
            cook_time=data['cook_time'],
            directions=data['directions'],
            user_id=current_user
        )

        recipe.save()

        return recipe.data, HTTPStatus.CREATED
    

class RecipeResource(Resource):

    @jwt_required(optional=True)
    def get(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if recipe.is_publish == False and recipe.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        return recipe.data, HTTPStatus.OK
    
    @jwt_required(optional=True)
    def put(self, recipe_id):
        data = request.get_json()
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message': 'Access is not Allowed'}, HTTPStatus.FORBIDDEN
        
        recipe.name = data['name']
        recipe.description = data['description']
        recipe.num_of_servings = data['num_of_servings']
        recipe.cook_time = data['cook_time']
        recipe.directions = data['directions']

        recipe.save()

        return recipe.data, HTTPStatus.OK
    
    @jwt_required
    def delete(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message': 'Access is not Allowed'}, HTTPStatus.FORBIDDEN
        
        recipe.delete()
        return {}, HTTPStatus.NO_CONTENT

class RecipePublishResource(Resource):

    @jwt_required(optional=True)
    def put(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not Allowed'}, HTTPStatus.FORBIDDEN

        recipe.is_publish = True

        return {}, HTTPStatus.NO_CONTENT
    
    @jwt_required(optional=True)
    def delete(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not Allowed'}, HTTPStatus.FORBIDDEN
        
        recipe.is_publish = False
        return {}, HTTPStatus.NO_CONTENT
    