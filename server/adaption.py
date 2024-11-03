
import math
import scene
import random
import graphe

def init_museum(laScene) : 

  dx = 10
  dz = 10

  laScene.actor("toit","actor").add(scene.box("toit",50,0.1,50,"blanc")).add(scene.position(25,3,25))

  for i in range(0,5) : 
    for j in range(0,5):
      x = i*dx
      z = j*dz 
      suffixe = str(i)+"-"+str(j)
      nomSalle = "salle-" + suffixe
      mur_nord = "mur_nord_" + suffixe
      #laScene.actor(mur_nord, "actor").add(scene.panneau(mur_nord,8,3,"murBleu")).add(scene.position(x,0,z+4.9))
      #laScene.actor(nomSalle,"actor").add(scene.sphere(nomSalle,0.2,"vert")).add(scene.position(x,0,z))
      nomMurH = "H-"+suffixe
      laScene.actor(nomMurH,"actor").add(scene.wall(nomMurH,8,3,0.1,"murBleu")).add(scene.position(i*dx+dx/2,0,j*dz+dz/2))
      nomMurV = "V-"+suffixe
      laScene.actor(nomMurV,"actor").add(scene.wall(nomMurV,8,3,0.1,"murBleu")).add(scene.position(i*dx+dx/2,0,j*dz+dz/2)).add(scene.rotation(0,math.pi/2,0))

  #    scene.actor("sphere01","actor").add(sphere("sphere01",0.2,"vert")).add(position(2,0,2))
  #   scene.actor("box01","actor").add(box("box01",1,3,2,"blanc")).add(position(5,2,2))
  #    scene.actor("wall01","actor").add(wall("wall01",10,3,0.1,"murBriques")).add(position(10,0,10))
  #    scene.actor("wall02","actor").add(wall("wall02",10,3,0.1,"murBleu")).add(position(10,0,10)).add(rotation(0,3.14/2,0))   
  #   scene.actor("poster01","actor").add(poster("poster01",1,1,"./assets/240.jpg")).add(position(3,1.5,-0.2))
  #    scene.actor("poster02","actor").add(poster("poster02",1,1,"./assets/240.jpg")).add(position(3,1.5,-0.2)).add(anchoredTo("wall01"))   

  print(laScene.actors())


def random_artwork(i, j, laScene, leMusee) : 
  peintres = leMusee.peintres
  print(peintres)
  random.shuffle(peintres)
  peintre = peintres[0]
  res = []
  for objet in leMusee.tableaux.values() : 
    if objet.peintre == peintre : 
      url = objet.url
      hauteur = objet.hauteur
      largeur = objet.largeur
      print(objet.cle, largeur, hauteur, url)
      a = laScene.actor(objet.cle,"actor").add(scene.poster(objet.cle, largeur/100,hauteur/100,url))
      x = i*10 +(0.5 - random.random())*2 
      y = 2.0
      z = j*10 +(0.5 - random.random())*2 
      a.add(scene.position(x,y,z)) 
      a.add(scene.rotation(0, math.pi / 2, 0))  


def get_artworks_by_tag(repository, tag) :
  '''
  returns a set of artworks that have in common the tag in arguments 
  @params repository : the data structure holding the artworks 
  @params tag : the tag used to filter the artworks
  '''

  art_works = set()
  print("* iterate over the repository.")
  for key, value in repository.items() : 
    # print(f"Key: {key}, Value: {value}")
    if tag in value.tags : 
      art_works.add(value)

  return art_works

def getTablesByTag_taxonomie(graph, tag):
    tables = []
    start_node = graph.obtenirNoeudConnaissantNom(tag)
    
    def traverse(node):
        nonlocal tables
        if isinstance(node, graphe.Objet):
            # Check if the tableau is in self.niveaux[0]
            if node in graph.niveaux[0]:
                tables.append(node)
        
        for child_node in node.enfants:
            traverse(child_node)

    if start_node:
        # Traverse the graph to find tables associated with the given tag or its child tags
        traverse(start_node)

    return tables