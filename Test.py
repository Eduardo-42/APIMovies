from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Movies


fileName = './instance/Movies.db'
app = Flask(__name__)

# Configuración de SQLAlchemy
engine = create_engine(f'sqlite:///{fileName}')
Session = sessionmaker(bind=engine)

# Creamos las tablas al iniciar (si no existen)
Base.metadata.create_all(engine)

@app.route('/movies/bulk', methods=['POST'])
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
        # Mapeamos el array a objetos Movie
        nuevas_peliculas = [Movies(**peli) for peli in data]
        session.add_all(nuevas_peliculas)
        session.commit()
        return jsonify({"mensaje": f"Se insertaron {len(nuevas_peliculas)} peliculas"}), 201
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