from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from utils import hash_password
from models.user import User

from schemas.user import UserSchema


user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))


class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        data, errors = user_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': 'errors'}, HTTPStatus.BAD_REQUEST
        
        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST
        
        user = User(**data)
        user.save()
        return user_schema.dump(user).data, HTTPStatus.CREATED
        # username = json_data.get('username')
        # email = json_data.get('email')
        # non_hash_password = json_data.get('password')

        # if User.get_by_username(username):
        #     return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST
        
        # if User.get_by_email(email):
        #     return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST
        
        # password = hash_password(non_hash_password)
        
        # user = User(username=username,
        #             email=email,
        #             password=password)
        # user.save()

        # data = {
        #     'id': user.id,
        #     'username':user.username,
        #     'email': user.email
        # }

        # return data, HTTPStatus.CREATED
    

class UserResource(Resource):

    @jwt_required(optional=True)
    def get(self, username):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()
        if current_user == user.id:
            # data = {
            #     'id': user.id,
            #     'username': user.username,
            #     'email': user.email
            # }
            data = user_schema.dump(user).data
        else:
            # data = {
            #     'id': user.id,
            #     'username': user.username
            # }
            data = user_public_schema.dump(user).data

        return data, HTTPStatus.OK
    

class MeResource(Resource):

    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())
        # data = {
        #     'id': user.id,
        #     'username': user.username,
        #     'email': user.email
        # }
        # return data, HTTPStatus.OK
        return user_schema.dump(user).data, HTTPStatus.OK
    