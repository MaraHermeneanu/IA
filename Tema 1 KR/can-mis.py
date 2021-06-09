"""
Se va implementa o problema asemanatoare cu a canibalilor si misionarilor, indeplinind urmatoare conditii:
>>>Avem N1 canibali, N2 misionari si K unitati de hrana pe un mal (pe malul celalalt nu avem nimic) și o barcă cu M locuri.
 Ne intereseaza sa mutam toți canibalii si misionarii pe malul opus. Nu ne interesaza neaparat sa mutam si hrana.
>>>In cazul in care intr-unul dintre locuri (barca sau maluri) avem mai multi canibali decat misionari, acestia o sa-i atace.
Totusi misionarii pot evita sa fie atacati, hrandin canibalii cu unitati de hrana. Astfel, daca sunt NM (NM > 0) misionari
si NC canibali intr-o locatie si NC>NM, misionarii pot evita sa fie atacati de canibali hranindu-i cu (NC-NM)/2 unitati de hrana (practic un canibal se satura cu 0.5 unitati de hrana.
>>>Hrana poate fi mutata cu barca (dar trebuie mereu sa fie un om care carmuieste barca; barca nu se poate deplasa fara oameni).
O unitate de hrana ocupa loc cat un om (nu se pot deplasa decat unitati intregi de hrana, nu jumatati).
Canibalii nu mananca din hrana daca sunt singuri (doar un misionar le poate da, si le da numai daca e nevoie, adica daca sunt canibali mai multi decat misionari).
>>>In plus, barca se degradeaza in timp. La fiecare Nr deplasari cu barca (de la un mal la celalalt) un loc din barca se va degrada (adica numarul de locuri din barca scade cu 1). Se va preciza in afisarea solutiei, pentru fiecare tranziție si cate locuri au ramas in barca (adica locuri care nu s-au stricat).

>>>Costul unei mutări e dat de numărul de oameni din barcă
"""

import math as Math
import os
import sys
import time


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    graf = None  # contine graful problemei

    def __init__(self, info, parinte, nivel, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.nivel = nivel
        self.g = cost  # costul mutarii
        self.h = h
        self.f = self.g+self.h

    def obtineDrum(self):
        l = [self]  # lista predecesorilor
        nod = self
        while nod.parinte is not None:  # pana ajung la radacina
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def contineInDrum(self, infoNodNou):
        interesNodNou = infoNodNou[0:2]+infoNodNou[4:5] #optimizare - doar nr. canibali,misionari si malul
        nodDrum = self
        
        while nodDrum is not None: 
            interesNodDrum = nodDrum.info[0:2]+nodDrum.info[4:5] #optimizare - doar nr. canibali,misionari si malul
            if(interesNodNou == interesNodDrum):
                return True
            nodDrum = nodDrum.parinte
        return False

    def afisDrum(self, afisCost=False): 
        l = self.obtineDrum()
        sir = ""
        for nod in l:
            if nod.parinte is not None:
                if nod.parinte.info[4] == 1:
                    mbarca1 = self.__class__.graf.malInitial+'ic'
                    mbarca2 = self.__class__.graf.malFinal+'ic'
                    
                else:
                    mbarca1 = self.__class__.graf.malFinal+'ic'
                    mbarca2 = self.__class__.graf.malInitial+'ic'

                newL = max(0, self.__class__.graf.L-(nod.parinte.nivel-1)//self.__class__.graf.D)
                hr=0
                if nod.info[1]>0 and nod.info[0]>nod.info[1]: #canibali mai multi decat misionari -> i-am hranit in prealabil
                    hr = (nod.info[0]-nod.info[1])/2 #atat a fost consumat deja 

                print(">>> In barca mai sunt " + str(newL) + " locuri ")

                sir += ">>> In barca mai sunt " + str(newL) + " locuri\n"
                print(">>> Barca a plecat de pe malul {} la malul {} cu {} canibali si {} misionari si {} unitati de hrana.\n".format(mbarca1,
                      mbarca2, abs(nod.info[0]-nod.parinte.info[0]), abs(nod.info[1]-nod.parinte.info[1]), abs(nod.info[2]+hr-nod.parinte.info[2]))) 
                sir += ">>> Barca a plecat de pe malul {} la malul {} cu {} canibali si {} misionari si {} unitati de hrana.\n".format(mbarca1,
                      mbarca2, abs(nod.info[0]-nod.parinte.info[0]), abs(nod.info[1]-nod.parinte.info[1]), abs(nod.info[2]+hr-nod.parinte.info[2]))
            print(str(nod))
            sir += "\n"
            sir += str(nod)
            sir += "\n"
        if afisCost:
            sir += "Cost: " + str(self.g) + "\n"
            print("Cost: ", self.g)
        if afisCost:
            print("Nr noduri/Lungimea drumului: ", len(l))
            sir += "Nr noduri/Lungimea drumului: " + str(len(l)) + "\n"
        return sir


    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return(sir)

    def __str__(self):

        sir = ""
        sir += str(self.nivel)+")\n"

        if self.info[4] == 1:  # daca barca e pe malul initial
            canMalCurent = self.info[0]
            misMalCurent = self.info[1]
            hrMalCurent = self.info[2]
            
            canMalOpus = self.__class__.graf.C-canMalCurent
            misMalOpus = self.__class__.graf.M-misMalCurent
            hrMalOpus = self.info[3]
            

            mbarca1 = self.__class__.graf.malInitial+'ic'
            mbarca2 = self.__class__.graf.malFinal+'ic'

        else:  # daca barca e pe malul final
            canMalOpus = self.info[0]
            misMalOpus = self.info[1]
            hrMalOpus = self.info[2]
            
            canMalCurent = self.__class__.graf.C-canMalOpus
            misMalCurent = self.__class__.graf.M-misMalOpus
            hrMalCurent = self.info[3]
            

            mbarca1 = self.__class__.graf.malFinal+'ic'
            mbarca2 = self.__class__.graf.malInitial+'ic'

        sir += "Malul "+mbarca1+":\n"
        sir += "Canibali: {} Misionari: {} Hrana: {}\n".format(
            canMalCurent, misMalCurent, hrMalCurent)
        sir += "Malul "+mbarca2+":\n"
        sir += "Canibali: {} Misionari: {} Hrana: {}\n".format(
            canMalOpus, misMalOpus, hrMalOpus)

        sir += "############################################\n"

        return sir


class Graph:  # graful problemei
    def __init__(self, caleFisier):

        f = open(caleFisier, "r")
        textFisier = f.read()

        # sparg pe linii, deci listaLinii = ['N1=4', 'N2=4' , etc ]
        # vreau sa construiesc listaInfoFisier de forma [N1,N2,K,M,Nr,MalInitial,MalFinal]

        listaParam = ['N1', 'N2', 'K', 'M', 'Nr', 'MalInitial', 'MalFinal']
        listaInfoFisier = [0] * len(listaParam)

        listaLinii = textFisier.split('\n')  # split pe linii
        for linie in listaLinii:
            valLinie = linie.strip().split('=')  # lista de 2 elem -> inainte si dupa egal

            # validare input - doar unitati intregi de mancare
            if valLinie[0].strip() not in listaParam:
                raise Exception("Fiser invalid (Parametrii)")
            if 'Mal' in valLinie[0] and valLinie[1].strip() not in ["est", "vest"]:
                raise Exception("Fiser invalid (Valorile pentru maluri)")
            if 'Mal' not in valLinie[0] and not(valLinie[1].strip().isnumeric()):
                raise Exception("Fiser invalid (Valori care nu sunt naturale)")

            listaInfoFisier[listaParam.index(valLinie[0].strip())] = valLinie[1].strip()
        #print(listaInfoFisier)

        self.__class__.C = int(listaInfoFisier[0])  # nr canibali ->N1
        self.__class__.M = int(listaInfoFisier[1])  # nr misionari ->N2
        self.__class__.K = int(listaInfoFisier[2])  # nr unitati hrana ->K
        self.__class__.L = int(listaInfoFisier[3])  # nr locuri in barca ->M
        self.__class__.D = int(listaInfoFisier[4])	# din cate in cate drumuri pierd cate un loc ->Nr
        self.__class__.malInitial = listaInfoFisier[5]  # mal initial
        self.__class__.malFinal = listaInfoFisier[6]  # mal final

        self.start = (self.__class__.C, self.__class__.M,self.__class__.K,0, 1)  # informatia nodului de start 
        #in forma [Canibali mal initial,Misionari mal initial, Hrana mal initial, Hrana mal final, Indicator barca la mal]

        self.scopuri = [(0, 0, 0)]

    def testeaza_scop(self, nodCurent):
        # ne intereseaza doar nr. can.,mis. si malul, nu si hrana
        # construiesc o noua lista, de forma [N1,N2,MalCurent] ( [Canibali,Misionari,Indicator mal] )

        listaInteres = nodCurent.info[0:2]+nodCurent.info[4:5]
        return listaInteres in self.scopuri

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent, tip_euristica="banala"):

        def test_conditie_mal(mis,can,hr):  # hr = nr unitati de hrana de pe mal  
            if mis == 0 or mis>=can:
                return True
            elif mis>0 and hr >= (can-mis)/2:
                return "se consuma hrana"
            else:
                return False
            
            #return mis == 0 or mis >=can or (can > mis and mis>0 and hr >= (can-mis)/2)

        def tupluri(suma):  # genereaza tripletele de o anumita suma a elementelor
            t = []
            for i in range(suma+1):
                for j in range(suma-i+1):

                    t.append((i, j, suma-i-j))
            return t

        def lista_info(lsucc): #obtine lista cu tuplurile info din fiecare nod din lista de succesori
            lista = []
            for succ in lsucc:
                lista.append(succ.info)
            return lista

        # nodCurent.info--> (CanibaliMalInitial, MisionariMalInitial, UnitHranaMalInitial, UnitHranaMalFinal, MalBarca/Indicator mal)
        # notam malCurent malul de unde pleaca barca si malOpus celalalt

        if nodCurent.info[4] == 1:  # daca barca e pe malul initial
            canMalCurent = nodCurent.info[0]
            misMalCurent = nodCurent.info[1]
            hrMalCurent = nodCurent.info[2]
            
            canMalOpus = self.__class__.C-canMalCurent
            misMalOpus = self.__class__.M-misMalCurent
            hrMalOpus = nodCurent.info[3]

        else:  # daca barca e pe malul final
            canMalOpus = nodCurent.info[0] #in nodul curent tin malul opus
            misMalOpus = nodCurent.info[1]
            hrMalOpus = nodCurent.info[2]
            
            canMalCurent = self.__class__.C-canMalOpus
            misMalCurent = self.__class__.M-misMalOpus
            hrMalCurent = nodCurent.info[3]

        # calculez care e numarul de locuri ramase
        # la D drumuri pierd cate un loc in barca

        #newL este noul numar de locuri din barca -> >= 0 
        newL = max(0, self.__class__.L-(nodCurent.nivel-1)//self.__class__.D)
        #din L (nr de locuri) scad cate locuri am pierdut in functie de lungimea drumului
    
        #maximul de oameni+hrana pe care il pot trimite
        maxOb = min(newL, Math.floor(canMalCurent+misMalCurent+hrMalCurent))

        listaSuccesori = []

        # in functie de cati oameni si mancare trimit
        for i in range(1, maxOb+1):
            config = tupluri(i)  # lista tuturor tripletelor de suma i
            
            for barca in config:
                # verific configuratia barcii
                
                # daca trimit mai mult decat am
                if barca[0] > canMalCurent or barca[1] > misMalCurent or barca[2] > hrMalCurent:
                    continue
                # daca am hrana fara oameni - triplete de forma (0,0,i)
                if barca[2] == i:
                    continue
                # daca am mai multi canibali decat misionari
                hrAjunge = barca[2]  #hrana care va ajunge de fapt
                if barca[0] > barca[1] and barca[1] > 0:
                    if barca[2] < (barca[0]-barca[1])/2:  # insuficienta mancare
                        continue
                    else:
                        hrAjunge = barca[2] - ((barca[0]-barca[1])/2) #hrana care va ajunge de fapt

                # motiv: daca sunt NM (NM > 0) misionari si NC canibali intr-o locatie si NC>NM,
                # misionarii pot evita sa fie atacati de canibali hranindu-i cu (NC-NM)/2 unitati de hrana
                # hrana nu poate fi transportata decat in unitati intregi

                # daca am ajuns aici inseamna ca configuratia barcii e ok, deci verific configuratia malurilor
                canMalCurentNou = canMalCurent-barca[0]
                misMalCurentNou = misMalCurent-barca[1]
                hrMalCurentNou = hrMalCurent-barca[2]
                
                canMalOpusNou = canMalOpus+barca[0]
                misMalOpusNou = misMalOpus+barca[1]
                hrMalOpusNou = hrMalOpus+hrAjunge

                # raman ok pe malul de pe care plec
                if not test_conditie_mal(misMalCurentNou, canMalCurentNou, hrMalCurentNou):
                    continue
                elif test_conditie_mal(misMalCurentNou,canMalCurentNou,hrMalCurentNou) == "se consuma hrana":
                    hrMalCurentNou -= (canMalCurentNou-misMalCurentNou)/2 #update hrana mal curent nou 
                
                # ajung ok pe celalalt mal
                if not test_conditie_mal(misMalOpusNou, canMalOpusNou, hrMalOpusNou):
                    continue
                elif test_conditie_mal(misMalOpusNou, canMalOpusNou, hrMalOpusNou) == "se consuma hrana":
                    hrMalOpusNou -= (canMalOpusNou-misMalOpusNou)/2 #update hrana mal opus nou

                # testul este pentru barca nodului curent (parinte) deci inainte de mutare
                if nodCurent.info[4] == 1:
                    infoNodNou = (canMalCurentNou,misMalCurentNou,hrMalCurentNou,hrMalOpusNou, 0)
                else:
                    infoNodNou = (canMalOpusNou, misMalOpusNou,hrMalOpusNou,hrMalCurentNou, 1)

                listinfo = lista_info(listaSuccesori)  #obtine lista cu tuplurile info din fiecare nod din lista de succesori
                    
                # daca nu era deja in lista de succesori
                if not nodCurent.contineInDrum(infoNodNou) and infoNodNou not in listinfo:
                    costSuccesor = barca[0]+barca[1] #costul unei mutari e dat de nr de oameni din barca
                    listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.nivel+1, cost=nodCurent.g +
                                          costSuccesor, h=NodParcurgere.graf.calculeaza_h(infoNodNou,newL,tip_euristica)))

        return listaSuccesori

    # euristica
    def calculeaza_h(self, infoNod,newL, tip_euristica="banala"):
        listaInteres = infoNod[0:2]+infoNod[4:5]
        if tip_euristica == "banala":
            if listaInteres not in self.scopuri:
                return 1
            return 0
        if tip_euristica == "1":
            #totalul de oameni de mutat 
            return (infoNod[0]+infoNod[1])+(1-infoNod[4])-1 

        if tip_euristica == "2":
            #cati oameni mai am de mutat impartit la nr de locuri din barca
            return Math.ceil((infoNod[0]+infoNod[1])/newL)

        if tip_euristica == "neadmisibila": 
            return infoNod[2]+infoNod[3]

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return(sir)


#UCS
def uniform_cost(graf, nrSolutiiCautate=1,timeout=300):
    timp_start = time.time()
    max_nod_memorie = 0
    total_succesori = 0
    f = open(output, "a")

    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(graf.start, None, 1, 0, graf.calculeaza_h(graf.start,graf.__class__.L))]
    f.write("Uniform Cost Search:\n")

    while len(c) > 0:
        timp_final = time.time()
        timp_exec = timp_final-timp_start
        if  timp_exec > timeout:
            print("Timpul maxim de executie a expirat.")
            f.write("Timpul maxim de executie a expirat.\n")
            return 

        if len(c)>max_nod_memorie:
            max_nod_memorie = len(c)

        # print("Coada actuala: " + str(c))
        # input()

        nodCurent = c.pop(0)

        if graf.testeaza_scop(nodCurent):
            print("Solutie:\n")
            f.write("Solutie:\n")
            sir = nodCurent.afisDrum(True)
            f.write(sir)
            f.write("Numarul maxim de noduri memorate: " + str(max_nod_memorie) + "\n")
            f.write("Numarul total de succesori calculati: " + str(total_succesori) + "\n")
            f.write("Timp de executie: " + str(round(timp_exec,2)) + " s\n")

            print("\n-----------------------------------------\n")
            f.write("\n-----------------------------------------\n")
            nrSolutiiCautate -= 1
            
            if nrSolutiiCautate == 0:
                return

        lSuccesori=graf.genereazaSuccesori(nodCurent)
        total_succesori+=len(lSuccesori)

        for s in lSuccesori:
            i=0
            gasit_loc=False
            for i in range(len(c)):
                # ordonez dupa cost(notat cu g aici și în desenele de pe site)
                if c[i].g>s.g :
                    gasit_loc=True
                    break
            if gasit_loc:
                c.insert(i,s)
            else:
                c.append(s)
    f.close()

#A*				
def a_star(graf, nrSolutiiCautate=1, tip_euristica="banala",timeout=300):
    timp_start = time.time()
    max_nod_memorie = 0
    total_succesori = 0
    f = open(output, "a")

    #in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c=[NodParcurgere(graf.start, None, 1,0, graf.calculeaza_h(graf.start,graf.__class__.L,tip_euristica=tip_euristica))]
    f.write("\n*****************************************")
    f.write("\nA* cu euristica "+ tip_euristica + ":\n")
    while len(c)>0:
        timp_final = time.time()
        timp_exec = timp_final-timp_start
        if  timp_exec > timeout:
            print("Timpul maxim de executie a expirat.")
            f.write("Timpul maxim de executie a expirat.\n")
            return 

        if len(c)>max_nod_memorie:
            max_nod_memorie = len(c)

        # print("Coada actuala: " + str(c))
        # input()
   
        nodCurent=c.pop(0)
        
        if graf.testeaza_scop(nodCurent):
            print("Solutie:\n")
            f.write("Solutie:\n")
            sir = nodCurent.afisDrum(True)
            f.write(sir)
            f.write("Numarul maxim de noduri memorate: " + str(max_nod_memorie) + "\n")
            f.write("Numarul total de succesori calculati: " + str(total_succesori) + "\n")
            f.write("Timp de executie: " + str(round(timp_exec,2)) + " s\n") 
            
            print("\n-----------------------------------------\n")
            f.write("\n-----------------------------------------\n")
            # input()
            nrSolutiiCautate-=1

            if nrSolutiiCautate==0:
                return

        lSuccesori=graf.genereazaSuccesori(nodCurent,tip_euristica)
        total_succesori+=len(lSuccesori)

        for s in lSuccesori:
            i=0
            gasit_loc=False
            for i in range(len(c)):
                #diferenta fata de UCS e ca ordonez dupa f
                if c[i].f>=s.f:
                    gasit_loc=True
                    break
            if gasit_loc:
                c.insert(i,s)
            else:
                c.append(s)


#A* optimizat
def a_star_optim(gr,tip_euristica="banala",timeout=300):
    timp_start = time.time()
    max_nod_memorie = 0
    total_succesori = 0    
    f = open(output, "a")

    #in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    l_open=[NodParcurgere(gr.start, None, 1,0, gr.calculeaza_h(gr.start, gr.__class__.L,tip_euristica=tip_euristica))]  
    #l_open contine nodurile candidate pentru expandare

    #l_closed contine nodurile expandate
    l_closed=[]
    f.write("\n*****************************************")
    f.write("\nA* optim cu euristica "+ tip_euristica + ":\n")
    while len(l_open)>0:
        timp_final = time.time()
        timp_exec = timp_final-timp_start
        if  timp_exec > timeout:
            print("Timpul maxim de executie a expirat.")
            f.write("Timpul maxim de executie a expirat.\n")
            return

        if len(l_open)>max_nod_memorie:
            max_nod_memorie = len(l_open)

        #print("Coada actuala: " + str(l_open))
        #input()

        nodCurent=l_open.pop(0)

        l_closed.append(nodCurent)
        if gr.testeaza_scop(nodCurent):
            print("Solutie:\n")
            f.write("Solutie:\n")
            sir = nodCurent.afisDrum(True)
            f.write(sir)
            f.write("Numarul maxim de noduri memorate: " + str(max_nod_memorie) + "\n")
            f.write("Numarul total de succesori calculati: " + str(total_succesori) + "\n")
            f.write("Timp de executie: " + str(round(timp_exec,2)) + " s\n")
                      
            print("\n-----------------------------------------\n")
            f.write("\n-----------------------------------------\n")
            return

        lSuccesori=gr.genereazaSuccesori(nodCurent,tip_euristica)	
        total_succesori+=len(lSuccesori)

        for s in lSuccesori:
            gasitC=False
            for nodC in l_open:
                if s.info==nodC.info:
                    gasitC=True
                    if s.f>=nodC.f:
                        lSuccesori.remove(s)
                    else:#s.f<nodC.f
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.info==nodC.info:
                        if s.f>=nodC.f:
                            print(s,lSuccesori)
                            lSuccesori.remove(s)
                            
                        else:#s.f<nodC.f
                            l_closed.remove(nodC)
                    break
        for s in lSuccesori:
            i=0
            gasit_loc=False
            for i in range(len(l_open)):
                #diferenta fata de UCS e ca ordonez crescator dupa f
                # daca f-urile sunt egale ordonez descrescator dupa g
                if l_open[i].f>s.f or (l_open[i].f==s.f and l_open[i].g<=s.g):
                    gasit_loc=True
                    break
            if gasit_loc:
                l_open.insert(i,s)
            else:
                l_open.append(s)
                                   

#IDA*
def ida_star(gr, nrSolutiiCautate=1,tip_euristica="banala",timeout=300):
    global tinceput
    timp_start = tinceput

    f = open(output, "a")
    f.write("\n*****************************************")
    f.write("\nIDA* cu euristica " + tip_euristica+ " \n")
    
    nodStart=NodParcurgere(gr.start, None, 1,0, gr.calculeaza_h(gr.start,gr.__class__.L,tip_euristica=tip_euristica))
    limita=nodStart.f
    
    while True:
        timp_final = time.time()
        timp_exec = timp_final-timp_start

        if  timp_exec > timeout:
            print("Timpul maxim de executie a expirat.")
            f.write("Timpul maxim de executie a expirat.\n")
            break 

        # print("Limita de pornire: ", limita)
        nrSolutiiCautate, rez= construieste_drum(f,gr, nodStart,limita,nrSolutiiCautate,tip_euristica)
        if rez=="gata":
            break
        if rez==float('inf'):
            print("Nu exista solutii!")
            f.write("Nu exista solutii.\n")
            break
        limita=rez

        # print(">>> Limita noua: ", limita)
        #input()
    f.close()


def construieste_drum(f,gr, nodCurent, limita, nrSolutiiCautate,tip_euristica):
    # print("A ajuns la: ", nodCurent)
    timp_nou = time.time()
    global tinceput
    global max_nod_memorie 
    global total_succesori 


    if nodCurent.f>limita:
        return nrSolutiiCautate, nodCurent.f

    if gr.testeaza_scop(nodCurent) and nodCurent.f==limita :

        print("Solutie:\n")
        f.write("Solutie:\n")
        sir = nodCurent.afisDrum(True)
        f.write(sir)
        f.write("Numarul maxim de noduri memorate: " + str(max_nod_memorie) + "\n")
        f.write("Numarul total de succesori calculati: " + str(total_succesori) + "\n")
        f.write("Timp de executie: " + str(round((timp_nou-tinceput),2)) + " s\n")
        print("\n-----------------------------------------\n")
        f.write("\n-----------------------------------------\n")
        max_nod_memorie = 0
        total_succesori = 0
            
        # print(limita)
        #input()
        nrSolutiiCautate-=1
        if nrSolutiiCautate==0:
            return 0,"gata"

    lSuccesori=gr.genereazaSuccesori(nodCurent,tip_euristica)	

    for succ in lSuccesori:
        drum = succ.obtineDrum()
        if len(drum)>max_nod_memorie:
            max_nod_memorie=len(drum)
    
    total_succesori+=len(lSuccesori)

    minim=float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez =construieste_drum(f,gr, s, limita, nrSolutiiCautate,tip_euristica)
        if rez=="gata":
            return nrSolutiiCautate,"gata"
        # print("Compara ", rez, " cu ", minim)
        if rez<minim:
            minim=rez
            # print("Noul minim: ", minim)
    return nrSolutiiCautate, minim


if len(sys.argv) == 5:
    caleInput = sys.argv[1]
    caleOutput = sys.argv[2]
    NSOL = int(sys.argv[3])
    timp = sys.argv[4]

elif len(sys.argv) == 4:
    caleInput = "Input"
    caleOutput = sys.argv[1]
    NSOL = int(sys.argv[2])
    timp = sys.argv[3]
else: 
    print("Apelul trebuie sa fie de forma: can-mis.py [cale input] [cale output] NSOL Timeout (MM:SS)\n sau, alternativ: can-mis.py [cale output] NSOL Timeout (MM:SS), folosindu-se implicit folderul Input")
    exit()


# #citesc calea input
# caleInput = input("Cale folder input: ")
# #print(caleInput)

# #citesc calea output
# caleOutput = input("Cale folder output: ")
# #print(caleOutput)

# #citesc nr sol
# NSOL = input("Numar solutii cautate: ")

# #citesc timpul maxim de cautare
# timp = input("Timp maxim de cautare in formatul MM:SS: ")




# #verific daca nu există folderul folder_output, caz în care îl creez
if not os.path.exists(caleOutput):
    os.mkdir(caleOutput)

t = timp.split(":")
minute=int(t[0])
secunde=int(t[1])
totalsecunde = minute*60+secunde

#pentru fiecare fisier de input creez un fisier de output
listaFisiere=os.listdir(caleInput)


#Var pt IDA*
max_nod_memorie = 0
total_succesori = 0
tinceput = 0

for numeFisier in listaFisiere:

    caleFisierIn = os.path.join(caleInput, numeFisier)

    gr = Graph(caleFisierIn)
    NodParcurgere.graf=gr

    numeFisierOutput="output_"+numeFisier

    caleFisierOut = caleOutput + "/" + numeFisierOutput

    output = caleFisierOut

    #UCS
    uniform_cost(gr,NSOL,totalsecunde)

    #A* euristica banala 
    a_star(gr,NSOL,"banala",totalsecunde)
    #A* euristica admisibila 1
    a_star(gr,NSOL,"1",totalsecunde)
    #A* euristica admisibila 2
    a_star(gr,NSOL,"2",totalsecunde)
    #A* euristica neadmisibila
    a_star(gr,NSOL,'neadmisibila',totalsecunde)


    #A* optim euristica banala 
    a_star_optim(gr,"banala",totalsecunde)
    #A* optim euristica admisibila 1
    a_star_optim(gr,"1",totalsecunde)
    #A* optim euristica admisibila 2
    a_star_optim(gr,"2",totalsecunde)
    #A* optim euristica neadmisibila
    a_star_optim(gr,'neadmisibila',totalsecunde)


    tinceput = time.time()
    #IDA* euristica banala 
    ida_star(gr,NSOL,"banala",totalsecunde)
    #IDA* euristica admisibila 1
    tinceput = time.time()
    ida_star(gr,NSOL,"1",totalsecunde)
    #IDA* euristica admisibila 2
    tinceput = time.time()
    ida_star(gr,NSOL,"2",totalsecunde)
    #IDA* euristica admisibila 2
    tinceput = time.time()
    ida_star(gr,NSOL,"neadmisibila",totalsecunde)

