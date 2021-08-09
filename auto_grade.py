#!/usr/bin/python3
# 1 Collecte élèves (nom, prenom, fichier_rendu), 2 Compilation + infos de compilation, 3 exécutions 
# des tests , 4 comptage de la documentation dans le code source, 5 rassembler les infos, 6 farbriguer le CSV
import subprocess

def nom_prenom(file_name_c):
    """
    Retrouve le prénom et le nom à partir du fichier C rendu.
    """
    nom_prenom = file_name_c[:-2]
    nom = nom_prenom.split('_')[0]
    prenom = nom_prenom.split('_')[1]
    return (nom, prenom)

def tests():
    """
    Effectue les 7 tests demandés et retourne le nombre de tests qui passent.
    """
    nb_tests_valide = 0
    for (a, b) in [(0, 0), (1, 0), (0, 1), (1, 1), (12, 12), (12, -43), (-1, -52)]:
        exec_test = subprocess.run(["./a.out", str(a), str(b)], stdout=subprocess.PIPE)
        if exec_test.stdout.decode() == "La somme de " + str(a) + " et " + str(b) + " vaut " + str(a+b) + "\n":
            nb_tests_valide += 1
    return nb_tests_valide

def commentaires(file_name_c):
    """
    Compte le nombre de commentaire dans le fichier.
    """
    com = subprocess.run(["grep", "eleves_bis/" + file_name_c, "-e", '/\*'], stdout=subprocess.PIPE)
    return com.stdout.decode().count("\n")


# RECUPERATION DE LA LISTE DE FICHIER C DANS LE REP...
ls = subprocess.run(["ls", "eleves_bis"], stdout=subprocess.PIPE)
Liste_eleve = ls.stdout.decode().split('\n')
Liste_eleve = Liste_eleve[:-1]
##############################################################

for file_name_c in Liste_eleve:
    nom, prenom = nom_prenom(file_name_c)
    gcc = subprocess.run(["gcc", "eleves_bis/"+file_name_c, "-Wall", "-ansi"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retour_gcc = gcc.stdout.decode()
    nb_warnings = retour_gcc.count("warning")
    nb_errors = retour_gcc.count("error")
    nb_comms = commentaires(file_name_c)
    bool_compil = 0
    note_compil = 0
    retour_test = 0

    if nb_errors == 0: #si la compilation produit un fichier exécutable
        bool_compil = 1
        note_compil = 3
        retour_test = tests()

    note_compil -= nb_warnings * 0.5
    if (note_compil < 0):
        note_compil = 0
    
    note_final = round(note_compil + (retour_test * 5/7) + (nb_comms * 2/3), 2)

    cmd_csv = ','.join([nom, prenom, str(bool_compil), str(nb_warnings), str(retour_test), str(nb_comms), str(note_compil), str(note_final)])
    subprocess.run("echo " + cmd_csv + " >> Notes.csv", shell=True)