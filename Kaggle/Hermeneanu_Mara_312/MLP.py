import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import plot_confusion_matrix


def normalize_data(train, test=None): #functie folosita pentru a normaliza datele
    scaler = preprocessing.StandardScaler()
    scaler.fit(train)
    scaler_training_data = scaler.transform(train)
    
    if test is not None:
        scaler_test_data = scaler.transform(test)
        return scaler_training_data, scaler_test_data

    return scaler_training_data


def read_from_txt(filename, foldername):

    imglist = [] 
    lablist = []

    with open(filename, "r") as file:
        lines = [line.strip() for line in file if line.strip()] #ignora liniile goale

    for line in lines:
        imglab = line.strip().split(',')  #liniile sunt de forma nume-image,label-imagine
        imglist.append(imglab[0]) #lista cu numele imaginilor 
        lablist.append(int(imglab[1])) #lista cu labeluri

    #afisarea catorva imagini
    # imagini = [Image.open('./'+ foldername+'/' +imgname) for imgname in imglist[:5]]
    # for img in imagini:
    #     img.show()

    #np array cu imaginile 
    x = np.array([np.array(Image.open('./'+ foldername+'/' +imgname)) for imgname in imglist])
    #print(x.shape)

    #np array cu labelurile
    y = np.array(lablist)

    return x,y

#citesc datele de train din fisier
x,y=read_from_txt("train.txt", "train") #print(y.shape)
#reshape
samples, w, h = x.shape  #x e de forma (15000,50,50)
x = x.reshape((samples,w*h)) #transform in (15000,2500) pentru functia de normalizare (am nevoie de dim 2)


#citesc datele de validare din fisier
x_val, y_val = read_from_txt("validation.txt", "validation")
#reshape
samples, w, h = x_val.shape #x e de forma (4500,50,50)
x_val = x_val.reshape((samples,w*h)) #transform in (4500,2500) pentru functia de normalizare (am nevoie de dim 2)


#normalizare date de train si validare
X,X_val = normalize_data(x,x_val)


#MLP MODEL
model = MLPClassifier(hidden_layer_sizes=(200,100,50),activation = 'relu',learning_rate = 'adaptive',max_iter = 2000, solver='adam')
model.fit(X, y) #training 
print('Acuratetea pe datele de train:', model.score(X, y))
print('Acuratetea pe datele de validare:', model.score(X_val, y_val))  

y_pred = model.fit(X, y).predict(X_val)

#confusion matrix si classification report
print(confusion_matrix(y_val, y_pred))
print(classification_report(y_val, y_pred))

#plot pentru confusion matrix 
plot_confusion_matrix(model, X_val, y_val)  
plt.show()  


#citesc datele de test din fisier
with open("test.txt", "r") as file:
    imgnames_test = [line.strip() for line in file if line.strip()] 

x_test = np.array([np.array(Image.open('./test/' +imgname)) for imgname in imgnames_test]) #np array cu imaginile de test

#reshape 
print(x_test.shape)
samples, w, h = x_test.shape # x_test e de forma (3900,50,50)
x_test = x_test.reshape((samples,w*h)) #transform in (3900,2500) pentru functia de normalizare (am nevoie de dim 2)

#normalizare date de test
X,X_test = normalize_data(x,x_test)

#predictii pentru test data 
y_test = model.predict(X_test) #predict 

#scriu imaginile si predictiile in fisier txt
predictions = open("submission-MLP.csv", "w")
predictions.write("id,label\n")

for index in range(len(imgnames_test)):
    predictions.write(imgnames_test[index]+","+str(y_test[index])+"\n")



