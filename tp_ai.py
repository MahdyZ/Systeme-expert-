import ai
from os import system
import os.path
from tkinter import *
from tkinter.ttk import *

faits=[]
conclusions=[]
premisses=[]
regles=[]
reglesutil=[]
f=""
fichier=""
ai.argPremisses=[]
ai.opPremisses=[]
ai.valPremisses=[]
ai.argFaits=[]
ai.valFaits=[]


def creationListe (fichier):
    regles = open(r"regles\{}.txt".format(fichier)).readlines()
    return regles

def creatListPremissesConclusions (conclusions,premisses,fichier):
    filepath = r"regles\{}.txt".format(fichier)
    premisse=[]
    try:
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
    except FileNotFoundError:
        print ("file not found")

def cretListFaits(faits,fichier):
    filepath = r"faits\{}.txt".format(fichier)
    with open(filepath) as fp:
        line = fp.readline()
        i = 0
        while line:
            if not(line.split("\n")[0] in faits):
                faits.append(line.split("\n")[0])
            line = fp.readline()
            i += 1

def saturer(faits,premisses,fichier,regles,reglesutil):
    f = open(r"trace.txt",'w')
    creatListPremissesConclusions(conclusions,premisses,fichier)
    changement=True
    brf=[]

    while changement==True:
        changement=False
        i=0
        while i < len(premisses):
            j=0
            while j < len(premisses[i]):
                existe=True
                if not (premisses[i][j] in faits):
                    existe=False
                    break
                j+=1
            if existe==True:
                if not (conclusions[i] in faits):
                    if not (regles[i] in reglesutil):
                        reglesutil.append(regles[i])
                    faits.append(conclusions[i])
                    changement=True
                    brf.append(regles[i])
            i+=1
    ai.ecrire(f,"************************\n****Règles utilisées****\n************************\n\n\n")
    for i in reglesutil:
        ai.ecrire(f,i)
    ai.ecrire(f,"\n\n\n**********************\n****Base des faits****\n**********************\n\n\n")        
    ai.ecrire(f,str(faits))
    #print(brf)

def chainage_avant_avec_but(faits,premisses,but):
    f = open(r"trace.txt",'w')
    ai.ecrire(f,"************************\n****Règles utilisées****\n************************\n\n\n")
    creatListPremissesConclusions(conclusions,premisses,fichier)
    changement=True
    find=False
    while changement and not find:
        changement=False
        if but in faits:
            find=True
            break
        i=0
        if but in faits:
            print("Le but '{}' existe déja dans la base des faits".format(but))
            break
        while i < len(premisses):
            j=0
            while j < len(premisses[i]):
                existe=True
                if not (premisses[i][j] in faits):
                    existe=False
                    break
                j+=1
            if existe==True:
                if not (conclusions[i] in faits):
                    faits.append(conclusions[i])
                    ai.ecrire(f,regles[i])
                    changement=True
                if but==conclusions[i]:
                    find=True
                    break
            i+=1
    ai.ecrire(f,"\n\n\n**********************\n****Base des faits****\n**********************\n\n\n")        
    ai.ecrire(f,str(faits))
    ai.ecrire(f,"\n\n")
    if find:
        ai.ecrire(f,"L'agorithme de chainage avant a atteint le but '{}'".format(but))
    else:
        ai.ecrire(f,"L'agorithme de chainage avant n'a pas atteint le but '{}'".format(but))

def filtrage(faits,premisses):
    brf=[]
    regles=creationListe(fichier)
    for regle in regles:
        for fait in faits:
            if fait in premisses:
                brf.append(regle)
    return brf

def chainage_avant_avec_conflit():
    brf=filtrage(faits,premisses)

def init (reglesutil,premisses,faits,conclusions):
    reglesutil=[]
    faits=[]
    premisses=[]
    conclusions=[]

if __name__ == '__main__':
    window = Tk()
    window.title("Systeme expert")
    window.geometry('370x200')
    selected = StringVar()
    direction = StringVar()
    text = StringVar()
    goal = IntVar()
    rad1 = Radiobutton(window,variable=selected,text='Maladies', value="maladies")
    rad2 = Radiobutton(window,variable=selected,text='Villes', value="villes")
    rad3 = Radiobutton(window,variable=selected,text='Meteorologies', value="meteorologies")
    rad4 = Radiobutton(window,variable=direction,text='Avant', value="avant")
    rad5 = Radiobutton(window,variable=direction,text='Arrière', value="arriere")
    rad6 = Radiobutton(window,variable=direction,text='Saturation', value="saturation")
    chk_state = BooleanVar()
    chk_state.set(False) #set check state
    chk = Checkbutton(window, text='Avec but:', var=chk_state)
    label = Label(window, text="But :")
    return0 = Entry(window, textvariable=text, width=30)
    def clicked():
        faits=[]
        regles=[]
        init(reglesutil,premisses,faits,conclusions)
        fichier=selected.get()
        direct=direction.get()
        boolean=chk_state.get()
        if direct=="avant":
            if not boolean:
                if not fichier in ["meteorologies",""]:
                    regles=creationListe(fichier) 
                    creatListPremissesConclusions(conclusions,premisses,fichier)
                    cretListFaits(faits,fichier)
                    print("chainage avant sans but")
                    saturer(faits,premisses,fichier,regles,reglesutil)
                elif fichier!="":
                    ai.creatListPremissesConclusions (ai.conclusions,ai.premisses,fichier)
                    ai.splitPremisses(ai.premisses)
                    ai.cretListFaits(ai.faits,fichier)
                    ai.splitFaits(ai.faits)
                    print("chainage avant sans but meteorologie")
                    ai.chainageAvant(ai.argPremisses,ai.opPremisses,ai.argFaits,ai.valFaits,ai.conclusions)
            else:
                if not fichier in ["meteorologies",""]:
                    regles=creationListe(fichier) 
                    creatListPremissesConclusions(conclusions,premisses,fichier)
                    cretListFaits(faits,fichier)
                    chainage_avant_avec_but(faits,premisses,text.get())
                elif fichier!="":
                    ai.creatListPremissesConclusions (ai.conclusions,ai.premisses,fichier)
                    ai.splitPremisses(ai.premisses)
                    ai.cretListFaits(ai.faits,fichier)
                    ai.splitFaits(ai.faits)
                    ai.chainageAvantAvecBut(ai.argPremisses,ai.opPremisses,ai.argFaits,ai.valFaits,ai.conclusions,text.get())
        elif direct=="arriere":
            print("pas encore developpé")
        else:
            if not boolean:
                if not fichier in ["meteorologies",""]:
                    regles=creationListe(fichier) 
                    creatListPremissesConclusions(conclusions,premisses,fichier)
                    cretListFaits(faits,fichier)
                    saturer(faits,premisses,fichier,regles,reglesutil)
                elif fichier!="":
                    ai.creatListPremissesConclusions (ai.conclusions,ai.premisses,fichier)
                    ai.splitPremisses(ai.premisses)
                    ai.cretListFaits(ai.faits,fichier)
                    ai.splitFaits(ai.faits)
                    print("Saturation de meteorolgie")
                    ai.saturation(ai.argPremisses,ai.opPremisses,ai.argFaits,ai.valFaits,ai.conclusions)
        #print(direction.get())
        #print(text.get())
        #print(chk_state.get())

    btn = Button(window, text="Appliquer", command=clicked)
    
    rad1.grid(column=0, row=0)
    rad2.grid(column=1, row=0)
    rad3.grid(column=2, row=0)
    rad4.grid(column=1, row=1)
    rad5.grid(column=2, row=1)
    rad6.grid(column=0, row=1)
    chk.grid(column=1, row=2)
    return0.grid(column=1,row=3)
    btn.grid(column=1, row=5)
    label.grid(row=3, column=0)
    window.mainloop()


#fichier="maladies"
#creatListPremissesConclusions(conclusions,premisses,fichier)
#cretListFaits(faits,fichier)
#saturer(faits,premisses)
#but="Végétation abondante = Vrai"
#chainage_avant_avec_but(faits,premisses,but)
#print("Les faits avec but:\n",faits)
#chainage_avant_avec_conflit()