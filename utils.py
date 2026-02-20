import requests
import json
import base64
import io
from PIL import Image




def searchMovieByTitle(title):

  urlMovies = f"https://api.imdbapi.dev/search/titles?query={title}"
  headers = {
      'content-type': 'application/json'
  }
  response = requests.get(urlMovies, headers=headers)
  data = response.json()
  titles = data['titles']

  return titles

def SearchMovieByIdAndImg(IDMBId, imageSize):
  movieDict = {}


  urlMovies = f"https://api.imdbapi.dev/titles/{IDMBId}"
  headers = {
      'content-type': 'application/json'
  }
  response = requests.get(urlMovies, headers=headers)
  data = response.json()

  imgUrl = data['primaryImage']['url']

  response = requests.get(imgUrl)
  response.raise_for_status()
  imageDownloaded = response.content

  base64Bytes = base64.b64encode(imageDownloaded)
  base64String = base64Bytes.decode('utf-8')

  if ',' in base64String:
      headers, encoded_data = base64String.split(',', 1)
  else:
      encoded_data = base64String

  image_bytes = base64.b64decode(encoded_data)
  img_buffer = io.BytesIO(image_bytes)
  img = Image.open(img_buffer)

  if imageSize:
    ancho_original, alto_original = img.size
   
  if ancho_original > imageSize:
    ratio = alto_original / ancho_original
    nuevo_alto = int(imageSize * ratio)
    img = img.resize((imageSize, nuevo_alto), Image.Resampling.LANCZOS)
  if img.mode in ("RGBA", "P"):
    img = img.convert("RGB")

  output_buffer = io.BytesIO()
  img.save(output_buffer, format="JPEG", quality=85)

  output_buffer.seek(0)
  new_base64_bytes = base64.b64encode(output_buffer.getvalue())
  new_base64_string = new_base64_bytes.decode('utf-8')


  movieDict['Titulo'] = data['primaryTitle']
  movieDict['Generos']=data['genres']
  movieDict['Rate']=data['rating']['aggregateRating']
  movieDict['Year']=data['startYear']
  movieDict['Summ']=data['plot']
  movieDict['Director']=data['directors'][0]['displayName']
  movieDict['Img']=new_base64_string

  return movieDict