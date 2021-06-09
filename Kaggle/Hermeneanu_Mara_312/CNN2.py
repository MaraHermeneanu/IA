import torch
import torchvision.transforms as torch_transf
from torch.utils.data import Dataset, DataLoader
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


class CTScanData(Dataset): 

    def __init__(self,input_file):
        #citesc datele din fisier
        imglist = [] 
        lablist = []

        with open(input_file, "r") as file:
            lines = [line.strip() for line in file if line.strip()] #pentru a ignora liniile goale

        for line in lines:
            imglab = line.strip().split(',')
            imglist.append(imglab[0]) #numele imaginii 
            if input_file != "test.txt":
                lablist.append(int(imglab[1])) #label-ul imaginii ca int


        #lista de imagini ca nparrays
        imgnp = [np.array(Image.open('./'+input_file.split(".")[0]+'/'+imgname)) for imgname in imglist]
        #print(x.shape)

        #normalizare
        norm = torch_transf.Normalize((0.5), (1)) 
        tens = torch_transf.ToTensor() 
        

        for i in range(len(imgnp)):
            imgnp[i] = norm(tens(imgnp[i]))

        self.x = imgnp #lista de tensori
        self.y = lablist #lista
        self.samples = len(imgnp)


    def __getitem__(self, index):
        if len(self.y)==0:
            return self.x[index]

        return self.x[index], self.y[index]

    def __len__(self):
        return self.samples


class CNN(torch.nn.Module):

    def __init__(self):
        super(CNN, self).__init__() #(W-F+2P)/S + 1
        self.conv1 = torch.nn.Conv2d(in_channels = 1, out_channels = 25, kernel_size = 2) #kernel = filter size = 3x3 stride=skipping  
        self.conv2 = torch.nn.Conv2d(in_channels = 25, out_channels = 50, kernel_size = 3)
        self.conv2_drop = torch.nn.Dropout2d(p=0.5) #impiedica overfitting-ul
        self.conv3 = torch.nn.Conv2d(in_channels = 50, out_channels = 100, kernel_size = 3) #padding ca imaginea sa nu devina prea mica si sa pastrez info din margini 
        self.conv3_drop = torch.nn.Dropout2d(p=0.4)
        self.conv4 = torch.nn.Conv2d(in_channels = 100, out_channels = 200, kernel_size = 5)

        self.fc1 = torch.nn.Linear(in_features=200*5*5,out_features= 2000)
        self.fc2 = torch.nn.Linear(in_features=2000, out_features=1000)
        self.fc3 = torch.nn.Linear(in_features=1000,out_features=3) #3 clase 

    def forward(self, x):

        x = torch.nn.functional.relu(torch.nn.functional.max_pool2d(self.conv1(x),2))
        x = torch.nn.functional.relu(torch.nn.functional.max_pool2d(self.conv2_drop(self.conv2(x)), 2)) #max pooling pe 2x2
        
        x = torch.nn.functional.relu(self.conv3_drop(self.conv3(x)))
        x = torch.nn.functional.relu(self.conv4(x))

        x = torch.flatten(x,1) #aplatizeaza toate dimensiunile mai putin dimensiunea batch-ului

        x = torch.nn.functional.relu(self.fc1(x))
        x = torch.nn.functional.relu(self.fc2(x))
        x = self.fc3(x)

        return torch.nn.functional.log_softmax(x,dim=1)

#initializare retea CNN
network = CNN()
optimizer = torch.optim.Adam(network.parameters(), lr=0.0009,amsgrad=True) #0.0007/9

#obiectele de tip dataset pentru data loaders
train_set = CTScanData("train.txt")
validation_set = CTScanData("validation.txt")
test_set = CTScanData("test.txt")

#data loaders
train_loader = DataLoader(
    train_set
    ,batch_size=100
    ,shuffle=True
)

validation_loader = DataLoader(
    validation_set
    ,batch_size=100
    ,shuffle=False
)

test_loader = DataLoader(
    test_set
    ,shuffle=False
)

trainloss_list=[]
validationloss_list=[]
accuracy_list=[]

for epoch in range(25):

    train_loss = 0 #pierederea totala pe datele de train
    validation_loss = 0  #pierderea totala pe datele de validare
    total_correct = 0 #numarul total de predictii corecte -> pt datele de validare 

    network.train()

    #training loop
    for batch in train_loader: 
        images, labels = batch 

        optimizer.zero_grad() #seteaza gradientii la 0 pentru a se face corect update-ul 

        preds = network(images) #predictions
        loss = torch.nn.functional.cross_entropy(preds, labels) # calculeaza pierderea
        
        loss.backward() # calculeaza gradientii
        optimizer.step() # update la ponderi/weights

        train_loss += loss.item() #adaug la train_loss

    network.eval() #calculez acuratetea

    
    for batch in validation_loader:
        
        images, labels = batch 

        preds = network(images) #predictions
        loss = torch.nn.functional.cross_entropy(preds, labels) # calculeaza pierderea
        
        # update-average-validation-loss 
        validation_loss += loss.item() 
        # numara cate predictii corecte 
        total_correct += np.count_nonzero(torch.max(preds, 1)[1] == labels) # torch.max(preds, 1) -> max pe linie si [1] pt lista cu indecsi

    print("epoch:", epoch, 
        "no. of correct predictions:", total_correct, 
        "train loss:", train_loss/len(train_loader),
        "validation loss:", validation_loss/len(validation_loader),
        "accuracy: ", 100*total_correct/len(validation_loader.sampler),"%")

    trainloss_list.append( train_loss/len(train_loader))
    validationloss_list.append(validation_loss/len(validation_loader))
    accuracy_list.append(100*total_correct/len(validation_loader.sampler))
    

#plot pentru loss    
plt.figure(1)    
plt.plot(trainloss_list,label="train loss", color="orange")
plt.legend()
plt.plot(validationloss_list,label="validation loss", color="blue")
plt.legend()
plt.show()
plt.figure(2)
plt.plot(accuracy_list,label="accuracy", color="red")
plt.legend()
plt.show()

predicted_test_labels = [] #label-urile pe care le voi prezice pentru datele de test 
with torch.no_grad(): #dezactivez calculul gradientilor
    for batch in test_loader: #images
        preds = network(batch)
        
        predicted_test_labels.extend(torch.max(preds, 1)[1].numpy()) # .numpy() tensor->numpy


#write predictions for test data in csv file
with open("test.txt", "r") as test_file:
    test_lines = [line.strip() for line in test_file if line.strip()] #pentru a ignora liniile goale



file_test_preds = open("submission-x.csv","w")
file_test_preds.write("id,label\n")

for i in range(len(test_lines)):
    file_test_preds.write(test_lines[i] + "," + str(predicted_test_labels[i]) + "\n")

file_test_preds.close()