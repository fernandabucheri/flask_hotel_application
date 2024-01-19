from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

# Recurso: contém as funções get, post, put, delete
class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} # SELECT * FROM hoteis
    
class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="Campo 'nome' não pode ficar em branco")
    argumentos.add_argument('estrelas', type=float, required=True, help="Campo 'estrelas' não pode ficar em branco")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    
    def get(self, hotel_id):
        hotel = HotelModel.encontrar_hotel(hotel_id)
        return hotel.json() if hotel else ({'message': 'Erro... Hotel não encontrado!'}, 404)
    
    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.encontrar_hotel(hotel_id):
            return {'message': f'ID \'{hotel_id}\' já está sendo usado.'}, 400
            
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.salvar_hotel()
        except:
            return {'message': 'Ocorreu um erro interno ao tentar salvar o hotel.'}, 500
        return hotel.json()
        
    # caso passe um id que já existe: edita
    # caso passe um id que não existe: cria
    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.encontrar_hotel(hotel_id)
        
        if hotel_encontrado: # editar
            hotel_encontrado.atualizar_hotel(**dados)
            hotel_encontrado.salvar_hotel()
            return hotel_encontrado.json(), 200
        
        # adicionar
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.salvar_hotel()
        except:
            return {'message': 'Ocorreu um erro interno ao tentar salvar o hotel.'}, 500
        return hotel.json(), 201

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.encontrar_hotel(hotel_id)
        
        if not hotel:
            return {'message': 'Hotel não encontrado.'}, 404
    
        try:
            hotel.deletar_hotel()
        except:
            return {'message': 'Ocorreu um erro interno ao tentar deletar o hotel.'}, 500
        return {'message': 'Hotel deletado.'}
    
    
'''
Notas:
novo_hotel = {'hotel_id': hotel_id, **dados} é a mesma coisa que 

novo_hotel = {
    'hotel_id': hotel_id,
    'nome': dados['nome'],
    'estrelas': dados['estrelas'],
    'diaria': dados['diaria'],
    'cidade': dados['cidade'],
}

**dados = kwargs

kwargs, nesse caso, são os argumentos definidos na classe
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
'''