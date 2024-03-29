from sql_alchemy import banco

class UserModel(banco.Model):
    __tablename__ = 'usuarios'
    
    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha
        
    def json(self):
        return {
            'user_id':self.user_id,
            'login': self.login    
        }
    
    @classmethod
    def encontrar_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first() # SELECT * FROM hoteis WHERE hotel_id = hotel_id
        return user if user else None
    
    @classmethod
    def encontrar_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        return user if user else None
    
    def salvar_user(self):
        banco.session.add(self)
        banco.session.commit()
    
    def deletar_user(self):
        banco.session.delete(self)
        banco.session.commit()
    
    