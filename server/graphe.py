import random 

class Noeud : 

  def __init__(self, nom, data, graphe):
    self.nom     = nom
    self.gr      = graphe
    self.niveau  = 1
    self.interet = round(random.random() * 10, 2) # 1.0
    self.parents = []
    self.enfants = []

  def charger(self, concepts, inventaire):
    pass
     
  def ajouterParent(self, noeud):
    self.parents.append(noeud)
    
  def ajouterEnfant(self, noeud):
    self.enfants.append(noeud)
    
  def consulterParents(self):
    return self.parents
    
  def consulterEnfants(self):
    return self.enfants
    
  def modifierInteret(self,interet):
    self.interet = interet
    
  def ajouterInteret(self, dInteret):
    self.interet += dInteret
    
  def consulterInteret(self):
    return self.interet
    
  def arc(self, noeud1, noeud2):
    return self.gr.arcs.get((noeud1.nom, noeud2.nom), None)
    
  def calculNiveau(self):
    if self.enfants == [] :
      return 0
    else:
      l = [noeud.calculNiveau() for noeud in self.enfants]
      self.niveau = 1 + max(l)
     # print(self.niveau)
      return self.niveau
      

      

class Objet(Noeud):
  def __init__(self, nom, tags, gr):
    Noeud.__init__(self,nom, tags, gr)
    self.tags     = tags
    self.niveau   = 0

  def calculInteret(self):
    if self.parents != [] : 
      self.interet = sum([p.consulterInteret() for p in self.consulterParents()])    

# ========================================================

class Graphe :

  def __init__(self):
    self.noeuds  = {}
    self.arcs    = {}
    self.root    = None
    self.niveaux = []

  def calculerObjetsLesPlusInteressants(self,n):
    # Sort the objects by interest in descending order
    sorted_objects = sorted(self.niveaux[0], key=lambda obj: obj.interet, reverse=True)

    # Take the top N objects and extract their names
    interesting_objects = [obj.nom for obj in sorted_objects[:num_objects]]

    # Check if there are no available artworks
    if not interesting_objects:
        print("There are no more available artworks")

    return interesting_objects

  def calculerInteretObjet(self ):
    pass

  def obtenirNoeudConnaissantNom(self,nom):
    return self.noeuds.get(nom, None)

  def consulterObjets(self):
    return self.niveaux[0]

  def consulterTags(self):
    return self.niveaux[1]

  def consulterNiveau(self,i):
    return self.niveaux[i]
    
  def montrerDoiNiveau(self,i):
    return dict((n.nom,n.doi) for n in self.niveaux[i])


  def ajouterNoeud(self, nom, data):
    if not nom in self.noeuds : 
      noeud = Noeud(nom, data, self)
      self.noeuds[noeud.nom] = noeud
      return noeud
    else:
      return self.noeuds[nom]

  def ajouterObjet(self, nom, data):
    if not nom in self.noeuds : 
      noeud = Objet(nom, data, self)
      self.noeuds[noeud.nom] = noeud
      return noeud
    else:
      return self.noeuds[nom]
  def ajouterArc(self, noeud1, noeud2, w):
    self.arcs[(noeud1.nom, noeud2.nom)] = w 	  
    noeud1.ajouterParent(noeud2)
    noeud2.ajouterEnfant(noeud1)
    
  def calculNiveau(self):
    n = self.root.calculNiveau() + 1
    

    self.niveaux = [[] for i in range(n+1)]
    for noeud in self.noeuds.values() : 
      #print(">>>> ", noeud.nom, " > ", noeud.niveau)
      self.niveaux[noeud.niveau].append(noeud)

  def interetObjets(self):
    pass

  def asynchrone(self,o):
    if isinstance(o, Objet) : 
      # print(f"Nodes : {self.noeuds.items()}")

      #
      # Calculate C 
      # 
      associated_tags = o.tags # V_plus_o
      tau = 0.2
      C = 0
      for key, value in self.noeuds.items() : 
        if not isinstance(value, Objet) : 
          C = sum(tau * self.noeuds[tag].interet for tag in self.noeuds)

      print(f"C : {C}")
      #
      # Calculate R 
      # 
      R = 0
      if len(associated_tags) != 0 : 
        R = C / len(associated_tags)

      print(f"R : {R}")

      # for el in self.noeuds.values() : 
      #   if not isinstance(el, Noeud) :
      #     print(f"In V_plus_o : {el}")
      D_I = 0

      for el in self.noeuds.values() : 
        if not isinstance(el, Objet) : 
          continue
        
        for tag in el.tags : 
          if tag in associated_tags : 
            D_I += R - tau * el.interet 
          else : 
            D_I -=  tau * el.interet 
        
        el.interet = D_I 

      # Recalculate the interest values for all objects
      for el in self.noeuds.values():
        if isinstance(el, Objet) : 
          el.calculInteret()
      
      I_values = [] # for discussing tau's influence
      for el in self.noeuds.values():   
        if isinstance(el, Objet) :        
          I_values.append(el.consulterInteret())
          print(f"Interet: {el.consulterInteret()}")
      
      self.writeInterest(I_values, "tau=0.5")
      
  def asynchrone_taxonomie(self, o) : 
    if isinstance(o, Objet) : 
      # print(f"Nodes : {self.noeuds.items()}")

      #
      # Calculate C 
      # 
      associated_tags = self.get_node_ancestors(o) # V_plus_o

      print(f"len V_plus_o : {len(associated_tags)}")
      print(f"V_plus_o : {associated_tags}")
      for tag in associated_tags : 
        print(f"tag : {tag}")
      tau = 0.2
      C = 0
      for key, value in self.noeuds.items() : 
        if not isinstance(value, Objet) : 
          C = sum(tau * self.noeuds[tag].interet for tag in self.noeuds)

      print(f"C : {C}")
      #
      # Calculate R 
      # 
      R = 0
      if len(associated_tags) != 0 : 
        R = C / len(associated_tags)

      print(f"R : {R}")

      # for el in self.noeuds.values() : 
      #   if not isinstance(el, Noeud) :
      #     print(f"In V_plus_o : {el}")
      D_I = 0

      for el in self.noeuds.values() : 
        if not isinstance(el, Objet) : 
          continue
        
        for tag in el.tags : 
          if tag in associated_tags : 
            D_I += R - tau * el.interet 
          else : 
            D_I -=  tau * el.interet 
        
        el.interet = D_I 

      # Recalculate the interest values for all objects
      for el in self.noeuds.values():
        if isinstance(el, Objet) : 
          el.calculInteret()
      
      I_values = [] # for discussing tau's influence
      for el in self.noeuds.values():   
        if isinstance(el, Objet) :        
          I_values.append(el.consulterInteret())
          print(f"Interet: {el.consulterInteret()}")
      
      # self.writeInterest(I_values, "tau=0.5")

  def synchrone(self):


    # Calculate I_avg

    I_avg = sum(el.consulterInteret() for el in self.noeuds.values() if isinstance(el, Objet))
    len_objs = sum(isinstance(el, Objet) for el in self.noeuds.values())

    # Avoid division by zero
    if len_objs > 0:
        I_avg /= len_objs

    # Amortization
    # sigma = random.random() # sigma in [0, 1]
    sigma = 0.5

    for el in self.noeuds.values():   
      if isinstance(el, Objet) :        
        if el.consulterInteret() > I_avg :
          el.interet = el.interet - sigma * (el.consulterInteret() - I_avg)
        elif el.consulterInteret() < I_avg : 
          el.interet = el.interet + sigma * (el.consulterInteret() - I_avg)
        
    

      
  def calculInteretMax(self):
    l = [noeud.interet for noeud in self.noeuds.values()]
    return max(l)
    
  def normalisationInteret(self):
    l = [noeud.interet for noeud in self.noeuds.values()]
    interetMax = max(l)
    for noeud in self.noeuds.values():
      noeud.interet = noeud.interet / doiMax
      
  def calculUpInteret(self):
    pass
        
  def calculDownInteret(self):
    pass


  def writeInterest(self, values, filename):
    with open(filename, 'w') as file:
        for value in values:
            file.write(str(value) + '\n')

  def get_node_ancestors(self, node):
      ancestors = set()

      def traverse_parents(current_node):
          nonlocal ancestors
          for parent in current_node.parents:
              ancestors.add(parent)
              traverse_parents(parent)

      traverse_parents(node)
      return ancestors