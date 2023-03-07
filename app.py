from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

#import library flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import os

#inisiasi object flask
app = Flask(__name__)

#insisasi object flask_restful
api = Api(app)

#inisiasi object flask_cors
CORS(app)

#inisiasi object flask_sqlalchemy
db = SQLAlchemy(app)

#mengkonfigurasi db
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database


#membuat database model
class ModelDatabase(db.Model):
    #membuat kolom tabel
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    umur = db.Column(db.Integer)
    alamat = db.Column(db.TEXT)

    #method untuk menyimpan data
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
        
#mengcreate Database        
db.create_all()

#inisiasi variable kosong bertipe dictionary
identitas = {} #variable global, dictionary = json

#membuat class resource
class contohResource(Resource):
    #method get dan post
    def get(self):
        # response = {"msg":"Hello, World!"}
        return identitas
    
    def post(self):
        dataNama = request.form["nama"]
        dataUmur = request.form["umur"]
        dataAlamat = request.form["alamat"]

        #masukan data kedalam database
        model = ModelDatabase(nama=dataNama, umur=dataUmur, alamat=dataAlamat)
        model.save()

        response = {
            "msg":"Data Berhasil Dimasukan",
            "code": 200
            }
        return response, 200
    
#setup resource
api.add_resource(contohResource, "/api", methods=["GET", "POST"]) 

if __name__ == "__main__":
    app.run(debug=True, port=5005)