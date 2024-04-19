import pycuber as pc
import readchar
import colorama
from colorama import Fore, Style

debug = False


def find_cycle(cube, start_letter,is_edge=True):

    if is_edge :
        ctype = "edge"
    else:
        ctype = "corner"

    if debug : print("New " + ctype + " cycle starting from " + start_letter)

    cycle = []

    # Sélectionner le bon mapping de couleurs basé sur le type de pièce
    if is_edge: #edge
        color_mapping = edge_color_mapping
        position_mapping = edge_position_mapping
    else:
        color_mapping = corner_color_mapping
        position_mapping = corner_position_mapping
    
    visited = []
    source_letter = start_letter
    cycle.append(source_letter)

    i=0
    while True:
        source_position = position_mapping[source_letter]
        visited.append(sorted(source_position))
        if debug : print("Récupération du Cubie en position " + source_position)
        source_colors = cube.colors(source_position)
        if debug : print("La pièce à la place " + source_letter + " ( position " + source_position + " ) a comme couleurs " + source_colors)
        
        target_letter = color_mapping[source_colors]
        if debug : print("Elle doit aller en position " + target_letter)

        cycle.append(target_letter)
        
        target_position = position_mapping[target_letter]        
        source_letter = target_letter

        if sorted(target_position) in visited:
            break

    return cycle,visited


def clean_cycle(cycle, letters_to_remove):
    letters_to_remove_set = set(letters_to_remove)
    
    # Étape 1: Supprimer les lettres spécifiées
    filtered_letters = [letter for letter in cycle if letter not in letters_to_remove_set]
    
    # Étape 2: Supprimer les lettres en double consécutives
    if not filtered_letters:
        return filtered_letters

    result = []
    i = 0
    while i < len(filtered_letters):
        # Si c'est le dernier élément ou différent du suivant, ajoutez-le
        if i == len(filtered_letters) - 1 or filtered_letters[i] != filtered_letters[i + 1]:
            result.append(filtered_letters[i])
            i += 1
        else:
            # Sautez les deux lettres s'ils sont identiques
            i += 2  # Incrémente de 2 pour passer au-delà de la paire identique

    return result


def format_sequence(sequence):
    # Sépare les suites de lettres par le ';'
    parts = sequence.upper().split(';')
    formatted_parts = []
    for part in parts:
        # Regroupe les lettres par deux, séparées par un espace
        grouped = ' '.join(part[i:i+2] for i in range(0, len(part), 2))
        formatted_parts.append(grouped)
    return ' ; '.join(formatted_parts)  # Rejoindre les deux parties avec ' ; '



def display_memory_training(sequence):
    colorama.init(autoreset=True)
    print("Sequence to memorize (corners;edges):")
    print(format_sequence(sequence))  # Affiche la séquence à mémoriser en majuscules
    print("Press spacebar to start ...")

    # Attendre que l'utilisateur appuie sur la barre d'espace
    while readchar.readkey() != readchar.key.SPACE:
        pass

    # Effacer les deux dernières lignes
    print("\033[A                                                          \033[A")  # Efface la dernière ligne
    print("\033[A                                                          \033[A")  # Efface la ligne avant la dernière
    print("\033[A                                                          \033[A")  # Efface la ligne avant la dernière

    print("Type memorized sequence (edges;corners), escape with 'Z' : ", end="", flush=True)
    user_input = ""

    # on inverse les séquences
    parts = sequence.upper().split(';')
    sequence = parts[1] + ";" + parts[0]

    errors = 0

    for expected_char in sequence.upper():
        while True:
            char = readchar.readkey().upper()  # Convertit la saisie en majuscule pour uniformité
            
            if char == 'Z':  # Interruption si 'Z' est tapée
                print(Fore.RED + "\nAbandon.")
                print(format_sequence(sequence))
                return

            if char == expected_char:
                print(Fore.GREEN + char, end="", flush=True)
                user_input += char
                break  # Sortie de la boucle interne si la lettre est correcte
            else:
                print(Fore.RED + char, end="", flush=True)  # Affiche la lettre en rouge
                errors += 1


    print()  # Pour le retour à la ligne après la saisie
    if user_input == sequence.upper():
        if errors == 0:
            print(Fore.GREEN + "Bravo !")
        else:
            print(Fore.MAGENTA + "Well done ! Only " + str(errors) + " errors.")



corner_position_mapping = {
    'A': 'ULB', 'B': 'UBR', 'C': 'URF', 'D': 'UFL',
    'E': 'LBU', 'F': 'LUF', 'G': 'LFD', 'H': 'LDB',
    'I': 'FLU', 'J': 'FUR', 'K': 'FRD', 'L': 'FDL',
    'M': 'RFU', 'N': 'RUB', 'O': 'RBD', 'P': 'RDF',
    'Q': 'BRU', 'R': 'BUL', 'S': 'BLD', 'T': 'BDR',
    'U': 'DLF', 'V': 'DFR', 'W': 'DRB', 'X': 'DBL'
}

faces_colors = {
    'U' : 'y',
    'L' : 'b',
    'F' : 'r',
    'R' : 'g',
    'B' : 'o',
    'D' : 'w'
}

corner_color_mapping = {}

for key, value in corner_position_mapping.items():
    colors = ""
    for face in value:
        colors += faces_colors[face]
    corner_color_mapping[colors] = key

edge_position_mapping = {
    'A': 'UB', 'B': 'UR', 'C': 'UF','D': 'UL',
    'E': 'LU', 'F': 'LF', 'G': 'LD', 'H': 'LB',
    'I': 'FU', 'J': 'FR', 'K': 'FD', 'L': 'FL',
    'M': 'RU', 'N': 'RB', 'O': 'RD', 'P': 'RF',
    'Q': 'BU', 'R': 'BL', 'S': 'BD', 'T': 'BR',
    'U': 'DF', 'V': 'DR', 'W': 'DB', 'X': 'DL'
}

edge_color_mapping = {}

for key, value in edge_position_mapping.items():
    colors = ""
    for face in value:
        colors += faces_colors[face]
    edge_color_mapping[colors] = key


if debug :
    print("Mappings :")
    print(corner_position_mapping)
    print(corner_color_mapping)
    print(edge_position_mapping)
    print(edge_color_mapping)

# Création d'un Rubik's Cube
cube = pc.Cube()

# Générer un mélange aléatoire
scramble = pc.Formula().random() # "R U R' U' L D2 R U2 B L' D2 F'" # 

cube(scramble)

print("Scramble:", scramble)
print(cube)


c_cycle,visited = find_cycle(cube,'E',False)
last_start_letter = 'A'
for start_letter,start_position in corner_position_mapping.items():
    if sorted(start_position) not in visited:
        new_cyle,new_visited = find_cycle(cube,start_letter,False)
        c_cycle += new_cyle
        visited += new_visited

# clean list
c_cycle = ''.join(clean_cycle(c_cycle,"AER"))
if debug : print(c_cycle)


e_cycle,visited = find_cycle(cube,'B',True)
last_start_letter = 'A'
for start_letter,start_position in edge_position_mapping.items():
    if sorted(start_position) not in visited:
        new_cyle,new_visited = find_cycle(cube,start_letter,True)
        e_cycle += new_cyle
        visited += new_visited

# clean list
e_cycle = ''.join(clean_cycle(e_cycle,"BM"))
if debug : print(e_cycle)

display_memory_training(c_cycle+";"+e_cycle)

