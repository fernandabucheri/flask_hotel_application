from flask_restful import Resource, reqparse
from models.usuario import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="O campo 'login' não pode ficar em branco.")
atributos.add_argument('senha', type=str, required=True, help="O campo 'senha' não pode ficar em branco."),

class User(Resource):
    def get(self, user_id):
        user = UserModel.encontrar_user(user_id)
        return user.json() if user else {'message': 'Erro... Usuário não encontrado!'}, 404
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.encontrar_user(user_id)
        
        if not user:
            return {'message': 'Usuário não encontrado.'}, 404
    
        try:
            user.deletar_user()
        except:
            return {'message': 'Ocorreu um erro interno ao tentar deletar o usuário.'}, 500
        return {'message': 'Usuário deletado.'}

class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()
        
        if UserModel.encontrar_login(dados['login']):
            return {'message': f'O login {dados["login"]} já existe.'}, 400
        
        user = UserModel(**dados)
        user.salvar_user()
        return {'message': 'Usuário cadastrado com sucesso!'}, 201
        
class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        
        user = UserModel.encontrar_login(dados['login'])
        
        # Gerando o hash da senha antes de salvar o usuário
        dados['senha'] = generate_password_hash(dados['senha'])
        
        if user and check_password_hash(dados['senha'], user.senha):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'message': 'Usuário ou senha foram digitados incorretamente.'}, 401
