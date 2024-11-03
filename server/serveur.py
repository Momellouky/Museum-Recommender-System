
import math
import random
import schedule
import time 

import scene
import musee
import adaption
import utils

import sqlite3
from  flask import Flask, jsonify, request

from flask_cors import CORS
app = Flask(import_name=__name__)
CORS(app)



graphe = {}


#scene = set()

def couleur(r,v,b):
    return {"r":r,"v":v,"b":b}


# =============================================================================================    
# La base de données Musée
# =============================================================================================





# =============================================================================================    
# Représentation 3d
# =============================================================================================



    

# ===========================================================================  

leMusee = musee.Musee("./assets/expo/","inventaire.json")    


    
@app.route('/assets')
def assets():
    materiaux = {}
    
    materiaux["rouge"] = {"color":[1,0,0]}
    materiaux["vert"]  = {"color":[0,1,0]} 
    materiaux["bleu"]  = {"color":[0,0,1]} 
    materiaux["blanc"] = {"color":[1,1,1], "texture":"./assets/textures/murs/dante.jpg","uScale":1,"vScale":1} ; 
    materiaux["murBriques"] = {"color":[1,1,1], "texture":"./assets/textures/murs/briques.jpg","uScale":2,"vScale":1} ;
    materiaux["murBleu"] = {"color":[1,1,1], "texture":"./assets/textures/murs/bleuCanard.jpg","uScale":2,"vScale":1} ; 
    materiaux["parquet"] = {"color":[1,1,1], "texture":"./assets/textures/sol/parquet.jpg","uScale":2,"vScale":2} ;   
    
    
    print(">>> ASSETS OK") 
    
    return jsonify(materiaux)

@app.route('/tictac')
def tictac():
  t = request.args.get("Time",default=0,type=float)
  print("tictac ",t)
  return jsonify([])


@app.route('/init')
def init():
    laScene = scene.Scene()
    
    adaption.init_museum(laScene)

    return jsonify(laScene.jsonify())
    



@app.route('/porte/')
def onPorte():
    laScene = scene.Scene() 
    nomPorte = request.args.get('Nom')
    print("La porte ", nomPorte, " a été sélectionnée")
    
    peintres = leMusee.peintres
    print(peintres)
    random.shuffle(peintres)
    peintre = peintres[0]
    res = []
    for objet in musee.tableaux.values() : 
      if objet.peintre == peintre : 
        url = objet.url
        hauteur = objet.hauteur
        largeur = objet.largeur
        a = laScene.actor(objet.cle,"actor").add(scene.poster(objet.cle, largeur/100,hauteur/100,url))
        x = (0.5 - random.random())*10 ; 
        y = 2.0
        z = (0.5 - random.random())*10 ;
        a.add(scene.position(x,y,z))
        
 
        
    
    
    
    return jsonify(laScene.jsonify())
    #return jsonify([])
    
    
@app.route('/salle/')
def onSalle():
  print("CHANGEMENTDE SALLE")
  i = request.args.get("I",default=0,type=int)
  j = request.args.get("J",default=0,type=int)
  print("CHANGEMENTDE SALLE : i=",i," - j=",j)
  
  laScene = scene.Scene() 

  ## Get random artworks in the database
  #
  adaption.random_artwork(i, j, laScene=laScene, leMusee=leMusee)
  #
  ## 

  # nodes = leMusee.graphe.noeuds
  # art_works = set()
  # rotation, k, counter = math.pi / 2 , 1, 0 # they will be used for artwork instantiatio in the scene
  # while len(art_works) == 0 : 
  #   random_node = random.choice(list(nodes.keys()))
  #   # art_works = adaption.get_artworks_by_tag(repository=leMusee.tableaux, tag=random_node)
  #   art_works = adaption.getTablesByTag_taxonomie(graph=leMusee.graphe, tag=random_node)
  # art_works = utils.Objet2Artwork(repository=leMusee.tableaux, objs=art_works)
  # for el in art_works :
  #    utils.put_artwork_in_scene(laScene=laScene, art_work=el, i=i, j=j, rotation=rotation, k=k, nbr_artworks= counter)
  #    rotation *= 2
  #    k += 1
  #    counter += 1
  
  return jsonify(laScene.jsonify())
    
@app.route('/click/')
def onClick():
    x = request.args.get('X', default=0,type=float)
    y = request.args.get('Y', default=0,type=float)
    z = request.args.get('Z', default=0,type=float)
    nomObjet = request.args.get('Nom')

    if nomObjet != None : 

        print("Objet sélectionné : ",nomObjet)
        print("Point d'intersection : ",x," - ", y ," - ",z)

        o = leMusee.graphe.obtenirNoeudConnaissantNom(nomObjet)
        # leMusee.graphe.asynchrone(o)
        leMusee.graphe.asynchrone_taxonomie(o)
        # schedule.every(1).seconds.do(leMusee.graphe.synchrone)

        # schedule.run_pending()

        return jsonify([])
    else : 
        return jsonify([])






if __name__ == "__main__" : 
    app.run(debug=True)
