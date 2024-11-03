import scene 
import random
import math 

OFFSET=2
ROTATION= - math.pi
def put_artwork_in_scene(laScene, art_work, i, j, k, nbr_artworks) : 
  
  if nbr_artworks > 3 : 
    i += 1
  url = art_work.url
  hauteur = art_work.hauteur
  largeur = art_work.largeur
  print(art_work.cle, largeur, hauteur, url)
  a = laScene.actor(art_work.cle,"actor").add(scene.poster(art_work.cle, largeur/100,hauteur/100,url))
  # x = i*10 +(0.5 - random.random())*2 
  # y = 2.0
  # z = j*10 +(0.5 - random.random())*2 
  x = (k * 0.6 + 10 * i)
  y = 2
  z = (k * 0.6 + 10 * j)
  a.add(scene.position(x,y,z))   
  a.add(scene.rotation(0, RotatePi(), 0))


def ValueMap() : 
  '''
  LiADJ stand for Linear Adjustement. Which is a function that rotates between 
  [-2, 0, 2]
  '''
  global OFFSET
  if OFFSET == 2:
      OFFSET = -2
      return OFFSET
  elif OFFSET == -2:
      OFFSET = 0
      return OFFSET
  elif OFFSET == 0:
      OFFSET = 2
      return OFFSET
  else:
      # You can decide the default return value for other cases
      return None
  

def RotatePi() : 

  global ROTATION
  if ROTATION == math.pi / 2:
    ROTATION = math.pi
    return ROTATION
  elif ROTATION == math.pi:
    ROTATION =  -math.pi / 2
    return ROTATION
  elif ROTATION == -math.pi / 2:
    ROTATION =  -math.pi
    return ROTATION
  elif ROTATION == -math.pi : 
     ROTATION = math.pi / 2
     return ROTATION
  else:
    # Handle other cases or return a default value
    return None
  

def Objet2Artwork(repository, objs) : 

  art_works = []
  for key, value in repository.items() : 
    # print(f"Key: {key}, Value: {value}")
    for el in objs : 
      #  print(f"el : {el.nom}, value name : {value.cle}")
       if el.nom == value.cle :
        print("Name is the same")
        art_works.append(value)

  return art_works