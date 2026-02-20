from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Movies
from utils import searchMovieByTitle, SearchMovieByIdAndImg


fileName = './instance/Movies.db'
app = Flask(__name__)

# Configuración de SQLAlchemy
engine = create_engine(f'sqlite:///{fileName}')
Session = sessionmaker(bind=engine)

# Creamos las tablas al iniciar (si no existen)
Base.metadata.create_all(engine)

@app.route('/movies/load', methods=['POST'])
def bulk_insert():

    data = request.json 
    
    if not data or not isinstance(data, list):
        return jsonify({"error": "Se esperaba un array de datos"}), 400
    
    for indice, peli in enumerate(data):
        if not 'id' in peli:
            return jsonify({
                "error": f"Error en el elemento {indice}: No se encontro elemento id en el payload"
            }), 400

    session = Session()
    try:
        for indice, peli  in enumerate(data):
            
            nuevas_peliculas = SearchMovieByIdAndImg(peli.get('id'),200)
            
            generos_Array = nuevas_peliculas['Generos']

            

            pelicula_dict = {
                "id": peli.get('id'),
                "titulo": nuevas_peliculas.get('Titulo'),
                "generos": ", ".join(generos_Array),
                "rate": nuevas_peliculas.get('Rate'),
                "year": nuevas_peliculas.get('Year'),
                "summary": nuevas_peliculas.get('Summ'),
                "director":nuevas_peliculas.get('Director'),
                "image":nuevas_peliculas.get('Img')}
            
            

            nueva_peli_objeto = Movies(**pelicula_dict)

            session.add(nueva_peli_objeto)
            session.commit()
            return jsonify({"mensaje": f"{nuevas_peliculas}"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/movies', methods=['GET'])
def get_movies():
    session = Session()
    peliculas = session.query(Movies).all()
    
    # Convertimos a lista de diccionarios para enviar como JSON
    resultado = []
    for p in peliculas:
        resultado.append({
            "titulo": p.titulo, 
            "director": p.director, 
            "rate": float(p.rate)
        })
    
    session.close()
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)