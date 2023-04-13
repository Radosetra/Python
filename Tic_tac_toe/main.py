import pygame

# Initialisation de Pygame
pygame.init()

# Définition de la taille de la fenêtre
largeur_fenetre = 300
hauteur_fenetre = 300
taille_case = 100

# Définition des couleurs
blanc = (255, 255, 255)
rouge = (255, 0, 0)

# Création de la fenêtre de jeu
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Tic Tac Toe")

# Dessiner la grille de jeu
def dessiner_grille(coordonnee,signe):
    for ligne in range(3):
        for colonne in range(3):
            pygame.draw.rect(fenetre, blanc, (colonne*taille_case, ligne*taille_case, taille_case, taille_case), 3)
            if coordonnee:
                if ligne == coordonnee[0] and colonne == coordonnee[1]:
                    if signe == "X" :
                        # Draw X
                        pygame.draw.line(fenetre, blanc, (colonne*taille_case+20, ligne*taille_case+20), (colonne*taille_case+taille_case-20, ligne*taille_case+taille_case-20), 5) # \
                        pygame.draw.line(fenetre, blanc, (colonne*taille_case+20, ligne*taille_case+taille_case-20), (colonne*taille_case+taille_case-20, ligne*taille_case+20), 5) # /
                    else :
                        # Draw O
                        pygame.draw.circle(fenetre, rouge, (colonne*taille_case+taille_case//2, ligne*taille_case+taille_case//2), taille_case//2-10, 5)

def isWinner(values,refs):
    for ref in refs:
        if all(elem in values for elem in ref):
            return True
    return False
           
solutions = [
    ["A","D","G"],
    ["B","E","H"],
    ["C","F","I"],
    ["G","H","I"],
    ["D","E","F"],
    ["A","B","C"],
    ["A","E","I"],
    ["G","E","C"]
]

players = [
    {
        "signe" : "X",
        "values" : []
    },
    {
        "signe" : "O",
        "values" : []
    },
    
    ]
currentPlayer = 0
running = True
countTourn = 0
coordonnee = []
signe = ""
flag = False

cells = []
for ligne in range(3):
    ligne_cells = []
    for colonne in range(3):
        rect = pygame.Rect(colonne*taille_case, ligne*taille_case, taille_case, taille_case)
        ligne_cells.append(rect)
    cells.append(ligne_cells)

cells_played = [
    [{"value":"A","check":0},{"value":"B","check":0},{"value":"C","check":0}],
    [{"value":"D","check":0},{"value":"E","check":0},{"value":"F","check":0}],
    [{"value":"G","check":0},{"value":"H","check":0},{"value":"I","check":0}]
    ]

# Boucle principale du jeu
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Récupérer la position actuelle de la souris
            mouse_pos = pygame.mouse.get_pos()

            # Parcourir les cases pour vérifier si la position de la souris est à l'intérieur d'une case
            for i in range(3):
                for j in range(3):
                    if cells[i][j].collidepoint(mouse_pos):
                        # La souris est à l'intérieur de la case (i, j)
                        # Faire quelque chose avec la case, par exemple la marquer comme jouée
                        if cells_played[i][j]["check"]:
                            # Case deja jouer
                            print("Cette case est déjà jouée !")
                            flag = True
                            break
                        else:
                            flag = False
                            elem = cells_played[i][j]
                            elem["check"] = True
                            coordonnee[0] = i
                            coordonnee[1] = j
                            signe = players[currentPlayer]["signe"]
                            players[currentPlayer]["values"].append(elem["value"])
                            dessiner_grille(coordonnee,signe)  # dessiner la grille après chaque clic
                            pygame.display.update()
                        
                        # compter le nombre de tours
                        countTourn += 1
                        if 3 <= countTourn < 9:
                            # Verification winner
                            if(isWinner(players[currentPlayer]["values"], solutions)):
                                print("Felicitation player",currentPlayer + 1)
                                exit(0)
                        elif(countTourn == 9):
                            print("Match Null :(")
                            exit(0)

            if not flag:
                if currentPlayer == 0:
                    currentPlayer = 1
                else:
                    currentPlayer = 0
            print("Tour player", currentPlayer + 1)
                
        if not coordonnee:
            print("Tour player", currentPlayer + 1)
            dessiner_grille(coordonnee,signe)
            coordonnee.append(-1)
            coordonnee.append(-2)
            pygame.display.update()