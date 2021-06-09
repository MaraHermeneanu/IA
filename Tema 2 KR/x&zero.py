import time
import pygame
import sys
import statistics as stats
from pygame.locals import *
nr_noduri_generate=0

class Joc:
    NR_COLOANE=10
    JMIN=None
    JMAX=None
    GOL='#'

    @classmethod
    def initializeaza(cls, display, NR_COLOANE=10, dim_celula=70):
        cls.display=display
        cls.dim_celula=dim_celula
        cls.x_img = pygame.image.load('ics.png').convert_alpha()
        cls.x_img = pygame.transform.scale(cls.x_img, (dim_celula,dim_celula))
        cls.zero_img = pygame.image.load('zero.png').convert_alpha()
        cls.zero_img = pygame.transform.scale(cls.zero_img, (dim_celula,dim_celula))
        cls.celuleGrid=[] #este lista cu patratelele din grid
        for linie in range(NR_COLOANE):
            for coloana in range(NR_COLOANE):              
                patr = pygame.Rect(coloana*(dim_celula+1), linie*(dim_celula+1), dim_celula, dim_celula)
                cls.celuleGrid.append(patr)

    def deseneaza_grid(self): # tabla de exemplu este ["#","x","#","0",......]

        for ind in range(len(self.matr)):
            linie=ind//self.NR_COLOANE
            coloana=ind%self.NR_COLOANE

            culoare=(255,255,255)

            pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind]) #alb = (255,255,255)
            if self.matr[ind]=='x':
                self.__class__.display.blit(self.__class__.x_img,(coloana*(self.__class__.dim_celula+1),linie*(self.__class__.dim_celula+1)))
            elif self.matr[ind]=='0':
                self.__class__.display.blit(self.__class__.zero_img,(coloana*(self.__class__.dim_celula+1),linie*(self.__class__.dim_celula+1)))
        pygame.display.flip() #obligatoriu pentru a actualiza interfata (desenul)

    #in functie de cine a castigat - coloreaza simbolurile castigatoare
    def coloreaza_win(self):
        for ind in range(len(self.matr)):
            linie=ind//self.NR_COLOANE
            coloana=ind%self.NR_COLOANE

            culoarewin=(60,179,113)
            culoare=(255,255,255)

            px = numara_puncte(self.matr,'x')
            p0 = numara_puncte(self.matr,'0')
            winner = 'x' if px > p0  else '0' if p0>px else "remiza"
            
            if self.matr[ind]=='x':
                if winner == "x":
                    pygame.draw.rect(self.__class__.display, culoarewin, self.__class__.celuleGrid[ind]) #verde
                else:
                    pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind]) #alb = (255,255,255)
                self.__class__.display.blit(self.__class__.x_img,(coloana*(self.__class__.dim_celula+1),linie*(self.__class__.dim_celula+1)))    
            elif self.matr[ind]=='0':
                if winner == "0":
                    pygame.draw.rect(self.__class__.display, culoarewin, self.__class__.celuleGrid[ind]) #verde
                else:
                    pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind]) #alb = (255,255,255)
                self.__class__.display.blit(self.__class__.zero_img,(coloana*(self.__class__.dim_celula+1),linie*(self.__class__.dim_celula+1)))
            else: 
                pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind]) #alb = (255,255,255)

        pygame.display.flip() #obligatoriu pentru a actualiza interfata (desenul)


    def __init__(self, tabla=None):
        self.matr=tabla or [self.__class__.GOL]*self.NR_COLOANE**2

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator==cls.JMIN else cls.JMIN

    def final(self): #returneaza True sau False, in functie daca jocul s-a terminat sau nu 
        # daca mai e un singur patratel liber sau nu mai sunt patratele libere
        if (self.__class__.GOL not in self.matr) or self.matr.count(self.__class__.GOL)==1:
            return True

        for i in range(len(self.matr)):
            for j in range(len(self.matr)):
                li = i//self.NR_COLOANE #linie i
                ci = i%self.NR_COLOANE #coloana i
                lj = j//self.NR_COLOANE #linie j
                cj = j%self.NR_COLOANE #coloana j
                if self.matr[i] == self.__class__.GOL and self.matr[j] == self.__class__.GOL \
                and ((li==lj and abs(ci-cj)==1) or (ci==cj and abs(li-lj)==1)): #spatii libere vecine pe orizontala sau verticala
                    if mutare_valida(self.matr,i,j): #as putea face o mutare
                        return False
        return True
        
         
    def mutari(self, jucator_opus):
        l_mutari=[]
        
        for i in range(len(self.matr)):
            for j in range(len(self.matr)):
                if  i!=j and self.matr[i]==self.__class__.GOL and self.matr[j]==self.__class__.GOL: #doi indici liberi
                    li = i//10 #linie i 
                    ci = i%10 #coloana i
                    lj = j//10 #linie j 
                    cj = j%10 #coloana j

                    if li==lj and abs(ci-cj)==1 and mutare_valida(self.matr,i,j): #aceeasi linie & coloane adiacente & mutare valida(vecine cu x si 0)
                        # fac o copie matricei initiale
                        matr_tabla_noua=list(self.matr)

                        #plasez cele doua simboluri
                        matr_tabla_noua[i]=jucator_opus
                        matr_tabla_noua[j]=jucator_opus

                        #adaug in lista de posibile mutari
                        l_mutari.append(Joc(matr_tabla_noua))

                    if ci==cj and abs(li-lj)==1 and mutare_valida(self.matr,i,j): #aceeasi coloana & linii adiacente & mutare valida(vecine cu x si 0)
                        # fac o copie matricei initiale
                        matr_tabla_noua=list(self.matr)

                        #plasez cele doua simboluri
                        matr_tabla_noua[i]=jucator_opus
                        matr_tabla_noua[j]=jucator_opus

                        #adaug in lista de posibile mutari
                        l_mutari.append(Joc(matr_tabla_noua))
        
        return l_mutari
                                
        
    def estimeaza_scor(self, adancime):
        final=self.final()
        px = numara_puncte(self.matr,'x') #punctele lui x
        p0 = numara_puncte(self.matr,'0') #punctele lui 0
        
        if final: 
            t_final = 'remiza' if px == p0 else 'x' if px>p0 else "0" #setez t_final in functie de cine are punctaj mai mare

            if t_final==self.__class__.JMAX :
                return 99+adancime
            elif t_final==self.__class__.JMIN:
                return -99-adancime
            elif t_final=='remiza':
                return 0
        elif self.__class__.JMAX=='x':
            return px-p0
        else:
            return p0-px

    def estimeaza_scor_2(self,adancime):
        final=self.final()
        px = numara_puncte(self.matr,'x') #punctele lui x 
        p0 = numara_puncte(self.matr,'0') #punctele lui 0
        
        if final: 
            t_final = 'remiza' if px == p0 else 'x' if px>p0 else "0" #setez t_final in functie de cine are punctaj mai mare

            if t_final==self.__class__.JMAX :
                return 99+adancime
            elif t_final==self.__class__.JMIN:
                return -99-adancime
            elif t_final=='remiza':
                return 0
        else:
            return diag_deschise(self.matr,self.__class__.JMAX)-diag_deschise(self.matr,self.__class__.JMIN)
            
    def sirAfisare(self):
        sir="  |"
        sir+=" ".join([str(i) for i in range(self.NR_COLOANE)])+"\n"
        sir+="-"*(self.NR_COLOANE+1)*2+"\n"
        for i in range(self.NR_COLOANE): #itereaza prin linii
            sir+= str(i)+" |"+" ".join([str(x) for x in self.matr[self.NR_COLOANE*i : self.NR_COLOANE*(i+1)]])+"\n"
        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()			



class Stare:
    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc=tabla_joc
        self.j_curent=j_curent
        
        #adancimea in arborele de stari
        self.adancime=adancime

        #parintele din arbore
        self.parinte = parinte

        #estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare=estimare
        
        #lista de mutari posibile din starea curenta
        self.mutari_posibile=[]
        
        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa=None


    def mutari(self):
        l_mutari=self.tabla_joc.mutari(self.j_curent)
        juc_opus=Joc.jucator_opus(self.j_curent)
        l_stari_mutari=[Stare(mutare, juc_opus, self.adancime-1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari
        
    
    def __str__(self):
        sir= str(self.tabla_joc) + "Jucator curent: "+self.j_curent+"\nUrmeaza sa mute: "+ Joc.jucator_opus(self.j_curent)+"\n"
        return sir
    
class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(105, 104, 83),culoareFundalSel=(76, 146, 103), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255), valoare=""):
        self.display = display
        self.left=left
        self.top=top
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


############# ecran initial ########################
def deseneaza_alegeri(display, tabla_curenta):

    algoritm = GrupButoane(
        top=210,
        left=235,
        listaButoane=[
            Buton(display=display, w=100, h=50, text="minmax", valoare="minmax"),
            Buton(display=display, w=100, h=50, text="alphabeta", valoare="alphabeta")
        ],
        indiceSelectat=1)
    simbol = GrupButoane(
        top=270,
        left=285,
        listaButoane=[
            Buton(display=display, w=50, h=30, text="x", valoare="x"),
            Buton(display=display, w=50, h=30, text="zero", valoare="0")
        ],
        indiceSelectat=0)
    dificultate = GrupButoane(
        top = 150, 
        left = 185,
        listaButoane=[
            Buton(display=display, w=100, h=50,text="incepator", valoare="incepator"),
            Buton(display=display, w=100, h=52,text="mediu", valoare="mediu"),
            Buton(display=display, w=100, h=50,text="avansat", valoare="avansat")
        ],
        indiceSelectat=0)
    optjoc = GrupButoane(
        top = 400, 
        left = 185,
        listaButoane=[
            Buton(display=display, w=100, h=50,text="P vs P", valoare="P vs P"),
            Buton(display=display, w=100, h=52,text="P vs PC", valoare="P vs PC"),
            Buton(display=display, w=100, h=50,text="PC vs PC", valoare="PC vs PC")
        ],
        indiceSelectat=1)

    ok = Buton(display=display, top=500, left=305, w=80, h=40, text="OK", culoareFundal=(200, 0, 55))


    algoritm.deseneaza()
    simbol.deseneaza()
    dificultate.deseneaza()
    ok.deseneaza()
    optjoc.deseneaza()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not algoritm.selecteazaDupacoord(pos):
                    if not simbol.selecteazaDupacoord(pos):
                        if not dificultate.selecteazaDupacoord(pos):
                            if not optjoc.selecteazaDupacoord(pos):
                                if ok.selecteazaDupacoord(pos):
                                    display.fill((0, 0, 0))  # stergere ecran
                                    tabla_curenta.deseneaza_grid()
                                    return algoritm.getValoare(), simbol.getValoare(), dificultate.getValoare(),optjoc.getValoare()
        pygame.display.update()

            
""" Algoritmul MinMax """

nr_noduri_generate=0

def min_max(stare,tipestimare=1):
    global nr_noduri_generate
    if tipestimare==1:
        if stare.adancime==0 or stare.tabla_joc.final() :
            stare.estimare=stare.tabla_joc.estimeaza_scor(stare.adancime)
            return stare
    else: #2
        if stare.adancime==0 or stare.tabla_joc.final() :
            stare.estimare=stare.tabla_joc.estimeaza_scor_2(stare.adancime)
            return stare
        
    #calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile=stare.mutari()
    nr_noduri_generate+=len(stare.mutari_posibile)

    #aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare=[min_max(mutare,tipestimare) for mutare in stare.mutari_posibile]
    
    if stare.j_curent==Joc.JMAX :
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa=max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa=min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare=stare.stare_aleasa.estimare
    return stare 

def sort_stare(stare):
    return stare.tabla_joc.estimeaza_scor(stare.adancime)


""" Algoritmul  AlphaBeta"""

def alpha_beta(alpha, beta, stare,tipestimare=1):
    global nr_noduri_generate
    if tipestimare == 1:
        if stare.adancime==0 or stare.tabla_joc.final() :
            stare.estimare=stare.tabla_joc.estimeaza_scor(stare.adancime)
            return stare
    else: #2
        if stare.adancime==0 or stare.tabla_joc.final() :
            stare.estimare=stare.tabla_joc.estimeaza_scor_2(stare.adancime)
            return stare
    if alpha>beta:
        return stare #este intr-un interval invalid deci nu o mai procesez
    
    stare.mutari_posibile=stare.mutari()
    nr_noduri_generate+=len(stare.mutari_posibile) 


    if stare.j_curent==Joc.JMAX :

        estimare_curenta=float('-inf')

        #ordonez descrescator starile in functie de mutare pentru MAX
        mutari_sortate = sorted(stare.mutari_posibile, key=sort_stare,reverse=True)

        for mutare in mutari_sortate:
            #calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua=alpha_beta(alpha, beta, mutare,tipestimare)
            
            if estimare_curenta<stare_noua.estimare:
                stare.stare_aleasa=stare_noua
                estimare_curenta=stare_noua.estimare
            if alpha<stare_noua.estimare:
                alpha=stare_noua.estimare
                if alpha>=beta:
                    break

    elif stare.j_curent==Joc.JMIN :
        #ordonez crescator starile in functie de mutare pentru MAX
        mutari_sortate = sorted(stare.mutari_posibile, key=sort_stare)

        estimare_curenta=float('inf')
        
        for mutare in mutari_sortate:
            
            stare_noua=alpha_beta(alpha, beta, mutare,tipestimare)
            
            if estimare_curenta>stare_noua.estimare:
                stare.stare_aleasa=stare_noua
                estimare_curenta=stare_noua.estimare

            if beta>stare_noua.estimare:
                beta=stare_noua.estimare
                if alpha>=beta:
                    break
    stare.estimare=stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta): 
    final=stare_curenta.tabla_joc.final()
    if final: # daca jocul s-a terminat -> nu se mai pot face mutari
        px = numara_puncte(stare_curenta.tabla_joc.matr,'x') #punctele lui x
        p0 = numara_puncte(stare_curenta.tabla_joc.matr,'0') #punctele lui 0

        print("Remiza!") if px == p0 else print("A castigat x!") if px>p0 else print("A castigat 0!")
        return True

    return False

# """ Algoritmul  AlphaBeta"""
# # TODO DE ORDONAT BAZAT PE ESTIMARE ASTFEL INCAT ALPHA-BETA SA TAIE CAT MAI MULT DIN ARBORE

# def alpha_beta(alpha, beta, stare,tipestimare=1):
#     global nr_noduri_generate
#     if tipestimare == 1:
#         if stare.adancime==0 or stare.tabla_joc.final() :
#             stare.estimare=stare.tabla_joc.estimeaza_scor(stare.adancime)
#             return stare
#     else: #2
#         if stare.adancime==0 or stare.tabla_joc.final() :
#             stare.estimare=stare.tabla_joc.estimeaza_scor_2(stare.adancime)
#             return stare

    
#     if alpha>beta:
#         return stare #este intr-un interval invalid deci nu o mai procesez
    
#     stare.mutari_posibile=stare.mutari()
#     nr_noduri_generate+=len(stare.mutari_posibile) 


#     if stare.j_curent==Joc.JMAX :

#         estimare_curenta=float('-inf')
        
#         for mutare in stare.mutari_posibile:
#             #calculeaza estimarea pentru starea noua, realizand subarborele
#             stare_noua=alpha_beta(alpha, beta, mutare,tipestimare)
            
#             if estimare_curenta<stare_noua.estimare:
#                 stare.stare_aleasa=stare_noua
#                 estimare_curenta=stare_noua.estimare
#             if alpha<stare_noua.estimare:
#                 alpha=stare_noua.estimare
#                 if alpha>=beta:
#                     break

#     elif stare.j_curent==Joc.JMIN :
#         estimare_curenta=float('inf')
        
#         for mutare in stare.mutari_posibile:
            
#             stare_noua=alpha_beta(alpha, beta, mutare,tipestimare)
            
#             if estimare_curenta>stare_noua.estimare:
#                 stare.stare_aleasa=stare_noua
#                 estimare_curenta=stare_noua.estimare

#             if beta>stare_noua.estimare:
#                 beta=stare_noua.estimare
#                 if alpha>=beta:
#                     break
#     stare.estimare=stare.stare_aleasa.estimare

#     return stare
   


#obtine lista tutoror vecinilor -> linie+coloana+diagonale
def toti_vecinii(matrice,np):
    v = []
    # daca e coltul stg sus
    if np == 0:
        v.append(matrice[np+1])
        v.append(matrice[np+10])
        v.append(matrice[np+11])
    # daca e coltul dreapta sus        
    elif np==9:
        v.append(matrice[np-1])
        v.append(matrice[np+10])
        v.append(matrice[np+9])
    # daca e prima linie        
    elif np in range(1,9):
        v.append(matrice[np-1])
        v.append(matrice[np+1])
        v.append(matrice[np+10])
        v.append(matrice[np+11])
        v.append(matrice[np+9])
    # daca e coltul stg jos        
    elif np == 90:
        v.append(matrice[np-10])
        v.append(matrice[np+1])
        v.append(matrice[np-9])
    # daca e coltul dreapta jos
    elif np == 99:
        v.append(matrice[np-10])
        v.append(matrice[np-1])
        v.append(matrice[np-11])
    # daca e pe ultima linie        
    elif np in range(91,99):
        v.append(matrice[np-1])
        v.append(matrice[np+1])
        v.append(matrice[np-10])
        v.append(matrice[np-11])
        v.append(matrice[np-9])
    # daca e latura stg
    elif np in range(10,90,10):
        v.append(matrice[np+1])
        v.append(matrice[np+10])
        v.append(matrice[np-10])
        v.append(matrice[np+11])
        v.append(matrice[np-9])
    # daca e latura dreapta        
    elif np in range(19,99,10):
        v.append(matrice[np-1])
        v.append(matrice[np+10])
        v.append(matrice[np-10])
        v.append(matrice[np+9])
        v.append(matrice[np-11])
    #oriunde altundeva,in mijloc 
    else:
        v.append(matrice[np-1])
        v.append(matrice[np+1])
        v.append(matrice[np+10])
        v.append(matrice[np-10])
        v.append(matrice[np+11])
        v.append(matrice[np+9])
        v.append(matrice[np-11])
        v.append(matrice[np-9])
    return v    


#obtine lista vecinilor de pe linie si coloana
def vecini_linie_col(matrice,np): 
    v = []
    # daca e coltul stg sus
    if np == 0:
        v.append(matrice[np+1])
        v.append(matrice[np+10])
    # daca e coltul dreapta sus 
    elif np==9:
        v.append(matrice[np-1])
        v.append(matrice[np+10])
    # daca e prima linie   
    elif np in range(1,9):
        v.append(matrice[np-1])
        v.append(matrice[np+1])
        v.append(matrice[np+10])
    # daca e coltul stg jos   
    elif np == 90:
        v.append(matrice[np-10])
        v.append(matrice[np+1])
    # daca e coltul dreapta jos
    elif np == 99:
        v.append(matrice[np-10])
        v.append(matrice[np-1])
    # daca e pe ultima linie     
    elif np in range(91,99):
        v.append(matrice[np-1])
        v.append(matrice[np+1])
        v.append(matrice[np-10])
    # daca e latura stg
    elif np in range(10,90,10):
        v.append(matrice[np+1])
        v.append(matrice[np+10])
        v.append(matrice[np-10])
    # daca e latura dreapta      
    elif np in range(19,99,10):
        v.append(matrice[np-1])
        v.append(matrice[np+10])
        v.append(matrice[np-10])
    #oriunde altundeva,in mijloc
    else:
        v.append(matrice[np-1])
        v.append(matrice[np+1])
        v.append(matrice[np+10])
        v.append(matrice[np-10])
    return v    

#verifica daca pentru indice exista un vecin liber pe linie/coloana
def vecin_liber(matrice,np): 
    vec = []
    vec = vecini_linie_col(matrice,np)  
    if "#" in vec:
        return True
    return False


#verifica daca o mutare e valida -> daca placuta e vecina cu un x si cu un 0
#primeste matricea, indicii simbolurilor vecine din matricea desfasurata
def mutare_valida(matrice,np1,np2):

    #construiesc un vector cu indicii vecini
    indici = [np1,np2]

    #vecinii placutei - lista de liste
    vec=[]

    for ind in indici:
        v = toti_vecinii(matrice,ind) #vecinii unui simbol

        if v.count("x")>=1 and v.count("0")>=1: # daca unul din indici e vecin cu ambele simboluri
            return True   

        vec.append(v) #adaug in lista de liste

    # daca unul din simboluri e vecin doar cu x si celalalt doar cu 0 sau invers
    if ('x' in vec[0] and '0' in vec[1]) or ('0' in vec[0] and 'x' in vec[1]):
        return True   
    return False
    

def diagonale(matrice,n):
    #din matrice defasurata fac lista de liste
    matrix=[]
    i=0
    while i<len(matrice):
        matrix.append(matrice[i:i+n])
        i+=n

    #construiesc lista de liste cu toate diagonalele
    diag=[]

    #diagonalele de deasupra diag secundara+diagonala secundara
    cn=n
    for k in range(1,n+1):
        d=[]
        for i in range(cn):
            d.append(matrix[i][n-i-k])
        diag.append(d)
        cn-=1

    #diagonalele de sub diag secundara
    c=1
    for k in range(0,n-1):
        d=[]
        for i in range(c,n):
            d.append(matrix[i][n-i+k])
        diag.append(d)
        c+=1

    #diagonalele de deasupra diag principala+diag principala
    cn=n
    for k in range(0,n):
        d=[]
        for i in range(cn):
            d.append(matrix[i][i+k])
        diag.append(d)
        cn-=1

    #diagonalele de sub diag principala
    c=1
    for k in range(1,n):
        d=[]
        for i in range(c,n):
            d.append(matrix[i][i-k])
        diag.append(d)
        c+=1
    
    return diag        
        
#functie care numara de cate ori apare un substring intr-un string, numarand si suprapunerile
#de exemplu aparitii_overlap("bbb","bb") va returna 2
def aparitii_overlap(string, substring): 
    count = start = 0
    while True:
        start = string.find(substring, start) + 1
        if start > 0:
            count+=1
        else:
            return count

#primeste o matrice si un simbol si numara punctele acumulate de acel simbol
def numara_puncte(matrice,simbol):
    scor=0

    #lista diagonalelor
    diag = diagonale(matrice,10)

    #construiesc secventa pe care vreau sa o caut pe diagagonale
    punct = [simbol,simbol,simbol] #stim ca la fiecare secventa de 3 simboluri vecine acumulam un punct
    strpunct = ''.join(punct) #convertesc la string

    for d in diag:
        strd=''.join(d) #convertesc diagonala (lista) la string 
        scor += aparitii_overlap(strd,strpunct) #calculez nr de aparitii cu overlap si adun in scor
    
    return scor
    

def afiseaza_scor(matrice):
    print("Scor pentru x: " , numara_puncte(matrice,'x'))
    print("Scor pentru 0: " , numara_puncte(matrice,'0'))


#o diagonala deschisa este o diagonala fara simbolul jucatorului opus
#pentru un simbol dat, numar cate diagonale deschise exista
#cponderea unei diagonale deschise va fi nr de simboluri de pe ea
def diag_deschise(matrice,simbol):
    diag = diagonale(matrice,10)
    diag_open = 0
    for d in diag:
        strd = ''.join(d)
        if len(d) >= 3 and Joc.jucator_opus(simbol) not in strd:
            pondere_diag = strd.count(simbol)
            diag_open += pondere_diag
    return diag_open

def main():

    nr_noduri_generate=0

    #durata maxima joc
    raspuns_valid=False
    while raspuns_valid==False:
        timp=input("\nDurata maxima a jocului (numar minute): ")
        try:
            TMAX=int(timp)
            raspuns_valid=True
        except ValueError:
            print("Valoarea introdusa trebuie sa fie int")
        
    #setari interfata grafica
    pygame.init()
    pygame.display.set_caption('Hermeneanu Mara - x si 0')

    #dimensiunea ferestrei in pixeli
    ecran=pygame.display.set_mode(size=(709,709))
    Joc.initializeaza(ecran)

    #initializare tabla
    config_init = ["#"] * 44 + ["x","0"] + ["#"] * 8 + ["x","0"] + ["#"] * 44
    tabla_curenta=Joc(config_init)

    #preluam setarile de joc de la butoane
    tip_algoritm,Joc.JMIN,dificultate,optjoc = deseneaza_alegeri(ecran,tabla_curenta)

    #simbolul calculatorului
    Joc.JMAX= '0' if Joc.JMIN == 'x' else 'x'

    print("Simbol ales de utilizator:", Joc.JMIN)
    print("Algoritm ales: ", tip_algoritm)
    print("Dificultatea aleasa:", dificultate)
    print("Modul de joc aleas:", optjoc+'\n')

    print("Tabla initiala:")
    print(str(tabla_curenta))
    
    #creare stare initiala
    #in functie de dificultate, adancimea maxima creste
    adancime = 1 if dificultate == 'incepator' else 2 if dificultate == 'mediu' else 3
    stare_curenta=Stare(tabla_curenta,'x',adancime)

    #afiseaza tabla initiala - 4 simboluri in centru
    tabla_curenta.deseneaza_grid()

    click1=False
    linies1=0
    cols1=0

    tinainte_juc=time.time()
    tinainte_joc = time.time()

    timp_pc=[]

    nr_mutari =[0,0]

    nr_noduri = []

    while True :
        tdupa_joc = time.time()

        if (tdupa_joc-tinainte_joc)//60 >=TMAX:
            print("Timpul pentru joc a expirat.")
            print("Scorul actual:")
            afiseaza_scor(stare_curenta.tabla_joc.matr) #afisez scor
            stare_curenta.tabla_joc.coloreaza_win() #colorez simbolul castigator
            print("Timpul total de joc: " ,(tdupa_joc-tinainte_joc)//60," minute") 
            if len(timp_pc):
                print("Timpul minim de gandire pentru PC: {} milisecunde \nTimpul maxim de gandire pentru PC: {} milisecunde \nTimpul mediu de gandire pentru PC: {} milisecunde \nMediana timpului de gandire pentru PC: {} milisecunde" \
                    .format(min(timp_pc),max(timp_pc),stats.mean(timp_pc),stats.median(timp_pc)))
            print("Numar total mutari PC: {}\nNumar total mutari utilizator: {}".format(nr_mutari[1],nr_mutari[0])) 
            if len(nr_noduri):
                print("Numarul minim de noduri generate: {}\nNumarul maxim de noduri generate: {}\nNumarul mediu de noduri generate: {}\nMediana numarului de noduri generate: {}"\
                    .format(min(nr_noduri),max(nr_noduri),stats.mean(nr_noduri),stats.median(nr_noduri))) 
            break

        if stare_curenta.j_curent==Joc.JMIN:
            if optjoc =="PC vs PC":
                #Mutare calculator pe post de MIN - cu a doua estimare 
                
                #preiau timpul in milisecunde de dinainte de mutare
                t_inainte=int(round(time.time() * 1000))
                nr_noduri_generate=0
                if tip_algoritm=='minmax':
                    stare_actualizata=min_max(stare_curenta,tipestimare=2)
                else: #tip_algoritm=='alphabeta'
                    stare_actualizata=alpha_beta(-500, 500, stare_curenta,tipestimare=2)

                stare_curenta.tabla_joc=stare_actualizata.stare_aleasa.tabla_joc

                #afisez numarul de noduri generate pentru  ultima mutare si adaung in vectorul cu numerele de noduri generate
                print("\nNumar de noduri generate: ",nr_noduri_generate)
                nr_noduri.append(nr_noduri_generate)

                #afisez estimarea 
                print("Estimarea calculatorului: ", Joc.estimeaza_scor_2(stare_curenta.tabla_joc,adancime))

                print("\nTabla dupa mutarea calculatorului:")
                print(str(stare_curenta))
                stare_curenta.tabla_joc.deseneaza_grid()
                afiseaza_scor(stare_curenta.tabla_joc.matr)

                #preiau timpul in milisecunde de dupa mutare si adaug in vectorul de timpi
                t_dupa=int(round(time.time() * 1000))
                print("Calculatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
                timp_pc.append(t_dupa-t_inainte)
                
                #testez daca jocul a ajuns intr-o stare finala si daca da, afisez scorul si statisticile
                if (afis_daca_final(stare_curenta)):
                    stare_curenta.tabla_joc.coloreaza_win() #colorez simbolul castigator
                    print("Timpul total de joc: ",(tdupa_joc-tinainte_joc)//60," minute")
                    if len(timp_pc):
                        print("Timpul minim de gandire pentru PC: {} milisecunde\nTimpul maxim de gandire pentru PC: {} milisecunde\nTimpul mediu de gandire pentru PC: {} milisecunde\nMediana timpului de gandire pentru PC: {} milisecunde"\
                            .format(min(timp_pc),max(timp_pc),stats.mean(timp_pc),stats.median(timp_pc))) 
                    print("Numar total mutari PC: {}\nNumar total mutari utilizator: {}".format(nr_mutari[1],nr_mutari[0]))
                    if len(nr_noduri):
                        print("Numarul minim de noduri generate: {}\nNumarul maxim de noduri generate: {}\nNumarul mediu de noduri generate: {}\nMediana numarului de noduri generate: {}"\
                            .format(min(nr_noduri),max(nr_noduri),stats.mean(nr_noduri),stats.median(nr_noduri))) 
                    break
                    
                #S-a realizat o mutare. Schimb jucatorul cu cel opus si cresc numarul de mutari pentru calculator
                nr_mutari[1]+=1
                stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)
                tinainte_juc = int(round(time.time() * 1000))

            else:     
                #Mutare jucator
                for event in pygame.event.get():
                    if event.type== pygame.QUIT:
                        pygame.quit() #inchide fereastra
                        
                        print("Utilizatorul a inchis jocul.")
                        afiseaza_scor(stare_curenta.tabla_joc.matr)
                        print("Timpul total de joc: ",(tdupa_joc-tinainte_joc)//60, " minute")
                        if len(timp_pc):
                            print("Timpul minim de gandire pentru PC: {} milisecunde \nTimpul maxim de gandire pentru PC: {} milisecunde\nTimpul mediu de gandire pentru PC: {} milisecunde\nMediana timpului de gandire pentru PC: {} milisecunde"\
                                .format(min(timp_pc),max(timp_pc),stats.mean(timp_pc),stats.median(timp_pc)))
                        print("Numar total mutari PC: {}\nNumar total mutari utilizator: {}".format(nr_mutari[1],nr_mutari[0])) 
                        if len(nr_noduri):
                            print("Numarul minim de noduri generate: {}\nNumarul maxim de noduri generate: {}\nNumarul mediu de noduri generate: {}\nMediana numarului de noduri generate: {}"\
                                .format(min(nr_noduri),max(nr_noduri),stats.mean(nr_noduri),stats.median(nr_noduri))) 
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN: #event de mouse
                        
                        pos = pygame.mouse.get_pos() #coordonatele clickului                    
                        for np in range(len(Joc.celuleGrid)):
                            
                            if Joc.celuleGrid[np].collidepoint(pos):#verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                                linie=np//10
                                coloana=np%10
                                
                                if click1==False:
                                    if stare_curenta.tabla_joc.matr[np] == Joc.GOL and vecin_liber(stare_curenta.tabla_joc.matr,np):
                                        click1=True

                                        #retin linia si coloana primului click
                                        linies1 = linie
                                        cols1 = coloana
                                                                            
                                else:
                                    if stare_curenta.tabla_joc.matr[np] == Joc.GOL and ((linie==linies1 and abs(coloana-cols1)==1) or (coloana==cols1 and abs(linie-linies1)==1)) \
                                    and mutare_valida(stare_curenta.tabla_joc.matr,linies1*10+cols1,np):

                                        #plasez simbolul pe "tabla de joc"
                                        stare_curenta.tabla_joc.matr[linies1*10+cols1]=Joc.JMIN
                                        stare_curenta.tabla_joc.matr[linie*10+coloana]=Joc.JMIN
                                        
                                        #afisarea starii jocului in urma mutarii utilizatorului
                                        print("\nTabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))                                    
                                        stare_curenta.tabla_joc.deseneaza_grid()
                                        afiseaza_scor(stare_curenta.tabla_joc.matr)

                                        
                                        tdupa_juc = int(round(time.time() * 1000))
                                        print("Utilizatorul a gandit timp de "+ str(tdupa_juc-tinainte_juc) +" milisecunde")

                                        #testez daca jocul a ajuns intr-o stare finala si daca da, afisez scorul si statisticile
                                        if (afis_daca_final(stare_curenta)):
                                            stare_curenta.tabla_joc.coloreaza_win()
                                            print("Timpul total de joc: ",(tdupa_joc-tinainte_joc)//60, " minute")
                                            if len(timp_pc):
                                                print("Timpul minim de gandire pentru PC: {} milisecunde\nTimpul maxim de gandire pentru PC: {} milisecunde\nTimpul mediu de gandire pentru PC: {} milisecunde\nMediana timpului de gandire pentru PC: {}"\
                                                    .format(min(timp_pc),max(timp_pc),stats.mean(timp_pc),stats.median(timp_pc))) 
                                            print("Numar total mutari PC: {}\nNumar total mutari utilizator: {}".format(nr_mutari[1],nr_mutari[0]))
                                            if len(nr_noduri):
                                                print("Numarul minim de noduri generate: {}\nNumarul maxim de noduri generate: {}\nNumarul mediu de noduri generate: {}\nMediana numarului de noduri generate: {}"\
                                                    .format(min(nr_noduri),max(nr_noduri),stats.mean(nr_noduri),stats.median(nr_noduri))) 
                                            break
                                            
                                        click1=False

                                        #S-a realizat o mutare. Schimb jucatorul cu cel opus si cresc numarul de mutari pentru jucator
                                        nr_mutari[0]+=1
                                        stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)

                                    else:
                                        click1=False        
        #------------------------------------------------------------------------------------------------------------------------------
        else:
            if optjoc =="P vs P":
                #Mutare jucator pe post de MAX
                for event in pygame.event.get():
                    if event.type== pygame.QUIT:
                        pygame.quit() #inchide fereastra
                        
                        print("Utilizatorul a inchis jocul.")
                        afiseaza_scor(stare_curenta.tabla_joc.matr)
                        print("Timpul total de joc: ",(tdupa_joc-tinainte_joc)//60, " minute")
                        if len(timp_pc):
                            print("Timpul minim de gandire pentru PC: {} milisecunde\nTimpul maxim de gandire pentru PC: {} milisecunde\nTimpul mediu de gandire pentru PC: {} milisecunde\nMediana timpului de gandire pentru PC: {} milisecunde"\
                                .format(min(timp_pc),max(timp_pc),stats.mean(timp_pc),stats.median(timp_pc)))
                        print("Numar total mutari PC: {}\nNumar total mutari utilizator: {}".format(nr_mutari[1],nr_mutari[0])) 
                        if len(nr_noduri):
                            print("Numarul minim de noduri generate: {}\nNumarul maxim de noduri generate: {}\nNumarul mediu de noduri generate: {}\nMediana numarului de noduri generate: {}"\
                                .format(min(nr_noduri),max(nr_noduri),stats.mean(nr_noduri),stats.median(nr_noduri))) 
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN: #event de mouse
                        
                        pos = pygame.mouse.get_pos() #coordonatele clickului                    
                        for np in range(len(Joc.celuleGrid)):
                            
                            if Joc.celuleGrid[np].collidepoint(pos):#verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                                linie=np//10
                                coloana=np%10
                                
                                if click1==False:
                                    if stare_curenta.tabla_joc.matr[np] == Joc.GOL and vecin_liber(stare_curenta.tabla_joc.matr,np):
                                        click1=True

                                        #retin linia si coloana primului click
                                        linies1 = linie
                                        cols1 = coloana
                                                                            
                                else:
                                    if stare_curenta.tabla_joc.matr[np] == Joc.GOL and ((linie==linies1 and abs(coloana-cols1)==1) or (coloana==cols1 and abs(linie-linies1)==1)) \
                                    and mutare_valida(stare_curenta.tabla_joc.matr,linies1*10+cols1,np):

                                        #plasez simbolul pe "tabla de joc"
                                        stare_curenta.tabla_joc.matr[linies1*10+cols1]=Joc.JMAX
                                        stare_curenta.tabla_joc.matr[linie*10+coloana]=Joc.JMAX
                                        

                                        #afisarea starii jocului in urma mutarii utilizatorului
                                        print("\nTabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))                                    
                                        stare_curenta.tabla_joc.deseneaza_grid()
                                        afiseaza_scor(stare_curenta.tabla_joc.matr)

                                        
                                        tdupa_juc = int(round(time.time() * 1000))
                                        print("Utilizatorul a gandit timp de "+ str(tdupa_juc-tinainte_juc) +" milisecunde")

                                        #testez daca jocul a ajuns intr-o stare finala si daca da, afisez scorul si statisticile
                                        if (afis_daca_final(stare_curenta)):
                                            stare_curenta.tabla_joc.coloreaza_win()
                                            print("Timpul total de joc: ",(tdupa_joc-tinainte_joc)//60, " minute")
                                            if len(timp_pc):
                                                print("Timpul minim de gandire pentru PC: {}\nTimpul maxim de gandire pentru PC: {}\nTimpul mediu de gandire pentru PC: {}\nMediana timpului de gandire pentru PC: {}"\
                                                    .format(min(timp_pc),max(timp_pc),stats.mean(timp_pc),stats.median(timp_pc))) 
                                            print("Numar total mutari PC: {}\nNumar total mutari utilizator: {}".format(nr_mutari[1],nr_mutari[0]))
                                            if len(nr_noduri):
                                                print("Numarul minim de noduri generate: {}\nNumarul maxim de noduri generate: {}\nNumarul mediu de noduri generate: {}\nMediana numarului de noduri generate: {}"\
                                                    .format(min(nr_noduri),max(nr_noduri),stats.mean(nr_noduri),stats.median(nr_noduri))) 
                                            break
                                            
                                        click1=False

                                        #S-a realizat o mutare. Schimb jucatorul cu cel opus si cresc numarul de mutari pentru jucator
                                        nr_mutari[0]+=1
                                        stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)

                                    else:
                                        click1=False        

            else:
                #Mutare calculator
                
                #preiau timpul in milisecunde de dinainte de mutare
                t_inainte=int(round(time.time() * 1000))
                nr_noduri_generate=0
                if tip_algoritm=='minmax':
                    stare_actualizata=min_max(stare_curenta)
                else: #tip_algoritm=='alphabeta'
                    stare_actualizata=alpha_beta(-500, 500, stare_curenta)

                stare_curenta.tabla_joc=stare_actualizata.stare_aleasa.tabla_joc

                #afisez numarul de noduri generate pentru  ultima mutare si adaung in vectorul cu numerele de noduri generate
                print("\nNumar de noduri generate: ",nr_noduri_generate)
                nr_noduri.append(nr_noduri_generate)

                #afisez estimarea 
                print("Estimarea calculatorului: ", Joc.estimeaza_scor(stare_curenta.tabla_joc,adancime))

                print("\nTabla dupa mutarea calculatorului")
                print(str(stare_curenta))
                stare_curenta.tabla_joc.deseneaza_grid()
                afiseaza_scor(stare_curenta.tabla_joc.matr)

                #preiau timpul in milisecunde de dupa mutare si adaug in vectorul de timpi
                t_dupa=int(round(time.time() * 1000))
                print("Calculatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
                timp_pc.append(t_dupa-t_inainte)
                
                #testez daca jocul a ajuns intr-o stare finala si daca da, afisez scorul si statisticile
                if (afis_daca_final(stare_curenta)):
                    stare_curenta.tabla_joc.coloreaza_win()
                    print("Timpul total de joc: ", (tdupa_joc-tinainte_joc)//60, " minute")
                    if len(timp_pc):
                        print("Timpul minim de gandire pentru PC: {} milisecunde\nTimpul maxim de gandire pentru PC: {} milisecunde\nTimpul mediu de gandire pentru PC: {} milisecunde\nMediana timpului de gandire pentru PC: {} milisecunde"\
                            .format(min(timp_pc),max(timp_pc),stats.mean(timp_pc),stats.median(timp_pc))) 
                    print("Numar total mutari PC: {}\nNumar total mutari utilizator: {}".format(nr_mutari[1],nr_mutari[0]))
                    if len(nr_noduri):
                        print("Numarul minim de noduri generate: {}\nNumarul maxim de noduri generate: {}\nNumarul mediu de noduri generate: {}\nMediana numarului de noduri generate: {}"\
                            .format(min(nr_noduri),max(nr_noduri),stats.mean(nr_noduri),stats.median(nr_noduri))) 
                    break
                    
                #S-a realizat o mutare. Schimb jucatorul cu cel opus si cresc numarul de mutari pentru calculator
                nr_mutari[1]+=1
                stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)
                tinainte_juc = int(round(time.time() * 1000))

        for event in pygame.event.get():
                pygame.display.update()
                pygame.event.pump()
                if event.type== pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    while True:
        pygame.event.wait()
        for event in pygame.event.get():
            if event.type== pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


if __name__ == "__main__" :
    main()
