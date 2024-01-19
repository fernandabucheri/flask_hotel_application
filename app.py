from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin
from sql_alchemy import banco
from flask_jwt_extended import JWTManager # Gerenciador de identificação do usuário

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
api = Api(app)
jwt = JWTManager(app)

# Inicializa o SQLAlchemy com o aplicativo Flask
banco.init_app(app)

# End-points
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')

# Cria o banco de dados antes de executar o aplicativo
if __name__ == '__main__':
    with app.app_context():
        banco.create_all()
    app.run(debug=True)
