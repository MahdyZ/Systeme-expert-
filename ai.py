from os import system
import os.path
argPremisses=[]
opPremisses=[]
valPremisses=[]
argFaits=[]
valFaits=[]
conclusions=[]
premisses=[]
faits=[]
regles=[]
f=''


def creatListPremissesConclusions (conclusions,premisses,fichier):
    #Création de la liste des premisses, règles et conclusions
    filepath = r"regles\{}.txt".format(fichier)
    del premisses[:]
    del regles[:]
    del conclusions[:]
    premisse=[]
    with open(filepath) as fp:
        line = fp.readline()
        i = 0
        while line:
            if line != "\n":
                regles.append(line)
                conclusions.append(line.split(" alors ")[1].split("\n")[0])
                premisse.append(line.split(" alors ")[0].split("si ")[1])
                premisses.append(premisse[i].split(" et "))
                i += 1
            line = fp.readline()   

def splitPremisses (premisses):
    #Création des listes contenant les arguments, les opérateurs et les valeurs des prémisses
    l=''
    temp=[]
    tempop=[]
    tempval=[]
    del argPremisses[:]
    del opPremisses[:]
    del tempval[:]
    del valPremisses[:]
    for l in premisses:
        for k in l:
            temp.append(k.split()[0])
            tempop.append(k.split()[1])
            tempval.append(k.split()[2])
        argPremisses.append(temp)
        opPremisses.append(tempop)
        valPremisses.append(tempval)
        temp=[]
        tempop=[]
        tempval=[]

def cretListFaits(faits,fichier):
    #création de la liste des faits
    filepath = r"faits\{}.txt".format(fichier)
    del faits[:]
    with open(filepath) as fp:
        line = fp.readline()
        i = 0
        while line:
            faits.append(line.split("\n")[0])
            line = fp.readline()
            i += 1

def splitFaits(faits):
    #création des liste contenants les arguments et les valeurs des faits
    l=''
    del argFaits[:]
    del valFaits[:]
    for l in faits:
        argFaits.append(l.split()[0])
        valFaits.append(l.split()[2])

def ecrire(f,chaine):
    #fonction d'écriture dans le fichier trace
    f = open(r"trace.txt",'a')
    f.write(str(chaine))
    f.close()

def chainageAvant(argPremisses,opPremisses,argFaits,valFaits,conclusions):
    #chainage avant
    f = open(r"trace.txt",'w')
    ecrire(f,"************************\n****Règles utilisées****\n************************\n\n\n")
    temp=[]
    tempreg=[]
    for l in faits:
        temp.append(l)
    i=0
    truth=False
    for l in argPremisses:
        j=0
        for k in l:
            if not (k in argFaits):
                break
            truth=False
            index=argFaits.index(k)
            if (valFaits[index].isnumeric() and valPremisses[i][j].isnumeric()):
                if opPremisses[i][j]==">":
                    truth=float(valFaits[index]) > float(valPremisses[i][j])
                elif opPremisses[i][j]==">=":
                    truth=float(valFaits[index]) >= float(valPremisses[i][j])
                elif opPremisses[i][j]=="<":
                    truth=float(valFaits[index]) < float(valPremisses[i][j])
                elif opPremisses[i][j]=="<=":
                    truth=float(valFaits[index]) <= float(valPremisses[i][j])
                elif opPremisses[i][j]=="=":
                    truth=float(valFaits[index]) == float(valPremisses[i][j])
                elif opPremisses[i][j]=="!=":
                    truth=float(valFaits[index]) != float(valPremisses[i][j])
            else:
                truth=valFaits[index]==valPremisses[i][j]
            if not (truth):
                break
            
            j+=1

        if truth:
            argFaits.append(conclusions[i].split()[0])
            valFaits.append(conclusions[i].split()[2])
            if not (conclusions[i] in faits):
                temp.append(conclusions[i])
            if not (regles[i] in tempreg):
                tempreg.append(regles[i])
        i+=1
    for l in tempreg:
        ecrire(f,l)
    ecrire(f,"\n\n\n**********************\n****Base des faits****\n**********************\n\n\n")
    ecrire(f,str(temp))
    ecrire(f,"\nchainage avant fini")

def chainageAvantAvecBut(argPremisses,opPremisses,argFaits,valFaits,conclusions,but):
    #chainage avant avec but
    f = open(r"trace.txt",'w')
    ecrire(f,"************************\n****Règles utilisées****\n************************\n\n\n")
    trouve=False
    changement=True
    while not trouve and changement:
        changement=False
        if but in faits:
            trouve=True
            break
        truth=False
        i=0
        for l in argPremisses:
            j=0
            for k in l:
                if not (k in argFaits):
                    break
                truth=False
                index=argFaits.index(k)
                if (valFaits[index].isnumeric() and valPremisses[i][j].isnumeric()):
                    if opPremisses[i][j]==">":
                        truth=float(valFaits[index]) > float(valPremisses[i][j])
                    elif opPremisses[i][j]==">=":
                        truth=float(valFaits[index]) >= float(valPremisses[i][j])
                    elif opPremisses[i][j]=="<":
                        truth=float(valFaits[index]) < float(valPremisses[i][j])
                    elif opPremisses[i][j]=="<=":
                        truth=float(valFaits[index]) <= float(valPremisses[i][j])
                    elif opPremisses[i][j]=="=":
                        truth=float(valFaits[index]) == float(valPremisses[i][j])
                    elif opPremisses[i][j]=="!=":
                        truth=float(valFaits[index]) != float(valPremisses[i][j])
                else:
                    truth=valFaits[index]==valPremisses[i][j]
                if not (truth):
                    break
                j+=1
            if truth and not (conclusions[i] in faits):
                argFaits.append(conclusions[i].split()[0])
                valFaits.append(conclusions[i].split()[2])
                faits.append(conclusions[i])
                ecrire(f,regles[i])
                changement=True
            i+=1
    
    ecrire(f,"\n\n\n**********************\n****Base des faits****\n**********************\n\n\n")
    ecrire(f,str(faits))
    if trouve:    
        ecrire(f,"\n{} est trouvé".format(but))
    else:
        ecrire(f,"\n\n{} n'est pas trouvé".format(but))

def saturation(argPremisses,opPremisses,argFaits,valFaits,conclusions):
    #Saturation
    f = open(r"trace.txt",'w')
    ecrire(f,"************************\n****Règles utilisées****\n************************\n\n\n")
    changement=True
    while changement:
        truth=False
        i=0
        changement=False
        for l in argPremisses:
            j=0
            for k in l:
                if not (k in argFaits):
                    break
                truth=False
                index=argFaits.index(k)
                if (valFaits[index].isnumeric() and valPremisses[i][j].isnumeric()):
                    if opPremisses[i][j]==">":
                        truth=float(valFaits[index]) > float(valPremisses[i][j])
                    elif opPremisses[i][j]==">=":
                        truth=float(valFaits[index]) >= float(valPremisses[i][j])
                    elif opPremisses[i][j]=="<":
                        truth=float(valFaits[index]) < float(valPremisses[i][j])
                    elif opPremisses[i][j]=="<=":
                        truth=float(valFaits[index]) <= float(valPremisses[i][j])
                    elif opPremisses[i][j]=="=":
                        truth=float(valFaits[index]) == float(valPremisses[i][j])
                    elif opPremisses[i][j]=="!=":
                        truth=float(valFaits[index]) != float(valPremisses[i][j])
                else:
                    truth=valFaits[index]==valPremisses[i][j]
                if not (truth):
                    break
                j+=1
            if truth and not (conclusions[i] in faits):
                argFaits.append(conclusions[i].split()[0])
                valFaits.append(conclusions[i].split()[2])
                faits.append(conclusions[i])
                ecrire(f,regles[i])
                changement=True
            i+=1
    ecrire(f,"\n\n\n**********************\n****Base des faits****\n**********************\n\n\n")
    ecrire(f,str(faits))
    ecrire(f,"\n\nSaturation finie")

#fichier="meteorologies"
#creatListPremissesConclusions (conclusions,premisses,fichier)
#splitPremisses(premisses)
#cretListFaits(faits,fichier)
#splitFaits(faits)
#print(len(argPremisses),len(opPremisses),len(argFaits),len(valFaits),len(conclusions))
#chainageAvant(argPremisses,opPremisses,argFaits,valFaits,conclusions)
#saturation(argPremisses,opPremisses,argFaits,valFaits,conclusions)
#but="hdj"
#chainageAvantAvecBut(argPremisses,opPremisses,argFaits,valFaits,conclusions,but)
