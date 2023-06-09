import os
import time
import subprocess
import fnmatch
import pandas as pd
import numpy as np
#import seaborn as sns
# import matplotlib.pyplot as plt
#from PIL import ImageFilter,Image
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from foodrec.settings import BASE_DIR

class KMeans:
    def __init__(self, k=3, max_iter=100):
        self.k = k
        self.max_iter = max_iter
        self.centroids = None
        
    def fit(self, X):
        # Initialize centroids randomly
        n_samples, n_features = X.shape
        self.centroids = np.random.rand(self.k, n_features)
        
        # Run k-means algorithm
        for i in range(self.max_iter):
            # Assign each data point to the nearest centroid
            distances = np.sqrt(((X - self.centroids[:, np.newaxis])**2).sum(axis=2))
            distances[~np.isfinite(distances)] = np.inf
            labels = np.argmin(distances, axis=0)
            
            # Update each centroid as the mean of all data points assigned to it
            for j in range(self.k):
                if np.sum(labels == j) == 0:
                    continue
                self.centroids[j] = np.mean(X[labels == j], axis=0)
    
    def predict(self, X):
        distances = np.sqrt(((X - self.centroids[:, np.newaxis])**2).sum(axis=2))
        labels = np.argmin(distances, axis=0)
        return labels


data=pd.read_csv(os.path.join(BASE_DIR ,"static/data/food.csv"))
Breakfastdata=data['Breakfast']
BreakfastdataNumpy=Breakfastdata.to_numpy()
                                   
Lunchdata=data['Lunch']
LunchdataNumpy=Lunchdata.to_numpy()
                                            
Dinnerdata=data['Dinner']
DinnerdataNumpy=Dinnerdata.to_numpy()
Food_itemsdata=data['Food_items']


def Weight_Loss(age,weight,height):
    breakfastfoodseparated=[]
    Lunchfoodseparated=[]
    Dinnerfoodseparated=[]
        
    breakfastfoodseparatedID=[]
    LunchfoodseparatedID=[]
    DinnerfoodseparatedID=[]
        
    for i in range(len(Breakfastdata)):
        if BreakfastdataNumpy[i]==1:
            breakfastfoodseparated.append( Food_itemsdata[i] )
            breakfastfoodseparatedID.append(i)
        if LunchdataNumpy[i]==1:
            Lunchfoodseparated.append(Food_itemsdata[i])
            LunchfoodseparatedID.append(i)
        if DinnerdataNumpy[i]==1:
            Dinnerfoodseparated.append(Food_itemsdata[i])
            DinnerfoodseparatedID.append(i)
        
    # retrieving Lunch data rows by loc method |
    LunchfoodseparatedIDdata = data.iloc[LunchfoodseparatedID]
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.T
    #print(LunchfoodseparatedIDdata)
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.iloc[Valapnd]
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.T
    #print(LunchfoodseparatedIDdata)

    # retrieving Breafast data rows by loc method 
    breakfastfoodseparatedIDdata = data.iloc[breakfastfoodseparatedID]
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.iloc[Valapnd]
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.T
        
        
    # retrieving Dinner Data rows by loc method 
    DinnerfoodseparatedIDdata = data.iloc[DinnerfoodseparatedID]
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.iloc[Valapnd]
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.T
        
    #calculating BMI
    bmi = weight/((height/100)**2) 
    agewiseinp=0
        
    for lp in range (0,80,20):
        test_list=np.arange(lp,lp+20)
        for i in test_list: 
            if(i == age):
                tr=round(lp/20)  
                agecl=round(lp/20)    

        
    #conditions
    bmiinfo=""    
    if ( bmi < 16):
        bmiinfo="According to your BMI, you are Severely Underweight"
        clbmi=4
    elif ( bmi >= 16 and bmi < 18.5):
        bmiinfo="According to your BMI, you are Underweight"
        clbmi=3
    elif ( bmi >= 18.5 and bmi < 25):
        bmiinfo="According to your BMI, you are Healthy"
        clbmi=2
    elif ( bmi >= 25 and bmi < 30):
        bmiinfo="According to your BMI, you are Overweight"
        clbmi=1
    elif ( bmi >=30):
        bmiinfo="According to your BMI, you are Severely Overweight"
        clbmi=0

    #converting into numpy array
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.to_numpy()
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.to_numpy()
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.to_numpy()
    ti=(clbmi+agecl)/2
    
     ## K-Means Based  Dinner Food
    Datacalorie=DinnerfoodseparatedIDdata[1:,1:len(DinnerfoodseparatedIDdata)]
    kmeans = KMeans(k=3, max_iter=100)
    X = np.random.rand(*Datacalorie.shape)
    kmeans.fit(X)
    labels = kmeans.predict(X)
    XValu=np.arange(0,len(labels))
    dnrlbl=labels

    ## K-Means Based  lunch Food
    Datacalorie=LunchfoodseparatedIDdata[1:,1:len(LunchfoodseparatedIDdata)]
    kmeans = KMeans(k=3, max_iter=100)
    X = np.random.rand(*Datacalorie.shape)
    kmeans.fit(X)
    labels = kmeans.predict(X)
    XValu=np.arange(0,len(labels))
    lnchlbl=labels
   
    ## K-Means Based  breakfast Food
    Datacalorie=breakfastfoodseparatedIDdata[1:,1:len(breakfastfoodseparatedIDdata)]
    kmeans = KMeans(k=3, max_iter=100)
    X = np.random.rand(*Datacalorie.shape)
    kmeans.fit(X)
    labels = kmeans.predict(X)
    XValu=np.arange(0,len(labels))
    brklbl=labels
    
    
    inp=[]
    ## Reading of the Dataet
    datafin=pd.read_csv(os.path.join(BASE_DIR ,"static/data/nutrition_distriution.csv"))

    ## train set
    dataTog=datafin.T
    bmicls=[0,1,2,3,4]
    agecls=[0,1,2,3,4]
    weightlosscat = dataTog.iloc[[1,2,7,8]]
    weightlosscat=weightlosscat.T
    weightgaincat= dataTog.iloc[[0,1,2,3,4,7,9,10]]
    weightgaincat=weightgaincat.T
    healthycat = dataTog.iloc[[1,2,3,4,6,7,9]]
    healthycat=healthycat.T
    weightlosscatDdata=weightlosscat.to_numpy()
    weightgaincatDdata=weightgaincat.to_numpy()
    healthycatDdata=healthycat.to_numpy()
    weightlosscat=weightlosscatDdata[1:,0:len(weightlosscatDdata)]
    weightgaincat=weightgaincatDdata[1:,0:len(weightgaincatDdata)]
    healthycat=healthycatDdata[1:,0:len(healthycatDdata)]
    
    
    weightlossfin=np.zeros((len(weightlosscat)*5,6),dtype=np.float32)
    weightgainfin=np.zeros((len(weightgaincat)*5,10),dtype=np.float32)
    healthycatfin=np.zeros((len(healthycat)*5,9),dtype=np.float32)
    t=0
    r=0
    s=0
    yt=[]
    yr=[]
    ys=[]
    for zz in range(5):
        for jj in range(len(weightlosscat)):
            valloc=list(weightlosscat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightlossfin[t]=np.array(valloc)
            yt.append(brklbl[jj])
            t+=1
     

    
    X_test=np.zeros((len(weightlosscat),6),dtype=np.float32)

    print('####################')
    
    #randomforest
    for jj in range(len(weightlosscat)):
        valloc=list(weightlosscat[jj])
        valloc.append(agecl)
        valloc.append(clbmi)
        X_test[jj]=np.array(valloc)*ti
    
    
    
    X_train=weightlossfin# Features
    y_train=yt # Labels

    #Create a Gaussian Classifier
    clf=RandomForestClassifier(n_estimators=100)
    
    #Train the model using the training sets y_pred=clf.predict(X_test)
    clf.fit(X_train,y_train)
    
    #print (X_test[1])
    X_test2=X_test
    y_pred=clf.predict(X_test)
    
    returndata=[]
    print ('SUGGESTED FOOD ITEMS ::')
    for ii in range(len(y_pred)):
        print(y_pred)
        if y_pred[ii]==2:     #weightloss
            findata=Food_itemsdata[ii]
            returndata.append(Food_itemsdata[ii])
            # if int(veg)==1:
            #     datanv=['Chicken Burger']
        # for it in range(len(datanv)):
        #     if findata==datanv[it]:
        #         pass

    returndata.append(bmi)
    returndata.append(bmiinfo)
    return returndata




def Weight_Gain(age,weight,height):
    breakfastfoodseparated=[]
    Lunchfoodseparated=[]
    Dinnerfoodseparated=[]
        
    breakfastfoodseparatedID=[]
    LunchfoodseparatedID=[]
    DinnerfoodseparatedID=[]
        
    for i in range(len(Breakfastdata)):
        if BreakfastdataNumpy[i]==1:
            breakfastfoodseparated.append( Food_itemsdata[i] )
            breakfastfoodseparatedID.append(i)
        if LunchdataNumpy[i]==1:
            Lunchfoodseparated.append(Food_itemsdata[i])
            LunchfoodseparatedID.append(i)
        if DinnerdataNumpy[i]==1:
            Dinnerfoodseparated.append(Food_itemsdata[i])
            DinnerfoodseparatedID.append(i)
        
    # retrieving rows by loc method |
    LunchfoodseparatedIDdata = data.iloc[LunchfoodseparatedID]
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.iloc[Valapnd]
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.T
    
        
    # retrieving rows by loc method 
    breakfastfoodseparatedIDdata = data.iloc[breakfastfoodseparatedID]
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.iloc[Valapnd]
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.T
        
        
    # retrieving rows by loc method 
    DinnerfoodseparatedIDdata = data.iloc[DinnerfoodseparatedID]
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.iloc[Valapnd]
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.T
        
    #claculating BMI
    bmi = weight/((height/100)**2)        

    for lp in range (0,80,20):
        test_list=np.arange(lp,lp+20)
        for i in test_list: 
            if(i == age):
                tr=round(lp/20)  
                agecl=round(lp/20)

    bmiinfo=""    
    #conditions

    if ( bmi < 16):
        bmiinfo="according to your BMI, you are Severely Underweight"
        clbmi=4
    elif ( bmi >= 16 and bmi < 18.5):
        bmiinfo="according to your BMI, you are Underweight"
        clbmi=3
    elif ( bmi >= 18.5 and bmi < 25):
        bmiinfo="according to your BMI, you are Healthy"
        clbmi=2
    elif ( bmi >= 25 and bmi < 30):
        bmiinfo="according to your BMI, you are Overweight"
        clbmi=1
    elif ( bmi >=30):
        bmiinfo="according to your BMI, you are Severely Overweight"
        clbmi=0


    
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.to_numpy()
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.to_numpy()
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.to_numpy()
    ti=(clbmi+agecl)/2 
    
    
       ## K-Means Based  Dinner Food
    Datacalorie=DinnerfoodseparatedIDdata[1:,1:len(DinnerfoodseparatedIDdata)]
    kmeans = KMeans(k=3, max_iter=100)
    X = np.random.rand(*Datacalorie.shape)
    kmeans.fit(X)
    labels = kmeans.predict(X)
    XValu=np.arange(0,len(labels))
    dnrlbl=labels

    ## K-Means Based  lunch Food
    Datacalorie=LunchfoodseparatedIDdata[1:,1:len(LunchfoodseparatedIDdata)]
    kmeans = KMeans(k=3, max_iter=100)
    X = np.random.rand(*Datacalorie.shape)
    kmeans.fit(X)
    labels = kmeans.predict(X)
    XValu=np.arange(0,len(labels))
    lnchlbl=labels
   
    ## K-Means Based  breakfast Food
    Datacalorie=breakfastfoodseparatedIDdata[1:,1:len(breakfastfoodseparatedIDdata)]
    kmeans = KMeans(k=3, max_iter=100)
    X = np.random.rand(*Datacalorie.shape)
    kmeans.fit(X)
    labels = kmeans.predict(X)
    XValu=np.arange(0,len(labels))
    brklbl=labels
    
    inp=[]
    ## Reading of the Dataet
    datafin=pd.read_csv(os.path.join(BASE_DIR ,"static/data/nutrition_distriution.csv"))
    # datafin.head(5)
    
    dataTog=datafin.T
    bmicls=[0,1,2,3,4]
    agecls=[0,1,2,3,4]
    weightlosscat = dataTog.iloc[[1,2,7,8]]
    weightlosscat=weightlosscat.T
    weightgaincat= dataTog.iloc[[0,1,2,3,4,7,9,10]]
    weightgaincat=weightgaincat.T
    healthycat = dataTog.iloc[[1,2,3,4,6,7,9]]
    healthycat=healthycat.T
    weightlosscatDdata=weightlosscat.to_numpy()
    weightgaincatDdata=weightgaincat.to_numpy()
    healthycatDdata=healthycat.to_numpy()
    weightlosscat=weightlosscatDdata[1:,0:len(weightlosscatDdata)]
    weightgaincat=weightgaincatDdata[1:,0:len(weightgaincatDdata)]
    healthycat=healthycatDdata[1:,0:len(healthycatDdata)]
    
    # in wg
    weightlossfin=np.zeros((len(weightlosscat)*5,6),dtype=np.float32)
    weightgainfin=np.zeros((len(weightgaincat)*5,10),dtype=np.float32)
    healthycatfin=np.zeros((len(healthycat)*5,9),dtype=np.float32)
    t=0
    r=0
    s=0
    yt=[]
    yr=[]
    ys=[]
    for zz in range(5):
        
        for jj in range(len(weightgaincat)):
            valloc=list(weightgaincat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightgainfin[r]=np.array(valloc)
            yr.append(lnchlbl[jj])
            r+=1
     
    
    X_test=np.zeros((len(weightgaincat),10),dtype=np.float32)

  
    # In[287]:
    for jj in range(len(weightgaincat)):
        valloc=list(weightgaincat[jj])
        valloc.append(agecl)
        valloc.append(clbmi)
        X_test[jj]=np.array(valloc)*ti
    
    
    X_train=weightgainfin# Features
    y_train=yr # Labels
    
   
    
    
    #Create a Gaussian Classifier
    clf=RandomForestClassifier(n_estimators=100)
    
    #Train the model using the training sets y_pred=clf.predict(X_test)
    clf.fit(X_train,y_train)
    
   
    X_test2=X_test
    y_pred=clf.predict(X_test)
    
    
    returndata=[]
    print("Suggested Food Item :: ")
    for ii in range(len(y_pred)):
        if y_pred[ii]==1: 
            print("now here")     #weightgain
            findata=Food_itemsdata[ii]
            print("i am hereeeeee")
            returndata.append(Food_itemsdata[ii])
            

    returndata.append(bmi)
    returndata.append(bmiinfo)
    return returndata                    

   



def Healthy(age,weight,height):
    breakfastfoodseparated=[]
    Lunchfoodseparated=[]
    Dinnerfoodseparated=[]
        
    breakfastfoodseparatedID=[]
    LunchfoodseparatedID=[]
    DinnerfoodseparatedID=[]
        
    for i in range(len(Breakfastdata)):
        if BreakfastdataNumpy[i]==1:
            breakfastfoodseparated.append( Food_itemsdata[i] )
            breakfastfoodseparatedID.append(i)
        if LunchdataNumpy[i]==1:
            Lunchfoodseparated.append(Food_itemsdata[i])
            LunchfoodseparatedID.append(i)
        if DinnerdataNumpy[i]==1:
            Dinnerfoodseparated.append(Food_itemsdata[i])
            DinnerfoodseparatedID.append(i)
        
    # retrieving rows by loc method |
    LunchfoodseparatedIDdata = data.iloc[LunchfoodseparatedID]
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.iloc[Valapnd]
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.T
        
    # retrieving rows by loc method 
    breakfastfoodseparatedIDdata = data.iloc[breakfastfoodseparatedID]
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.iloc[Valapnd]
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.T
        
        
    # retrieving rows by loc method 
    DinnerfoodseparatedIDdata = data.iloc[DinnerfoodseparatedID]
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.iloc[Valapnd]
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.T
        
    
    bmi = weight/((height/100)**2) 
    agewiseinp=0
        
    for lp in range (0,80,20):
        test_list=np.arange(lp,lp+20)
        for i in test_list: 
            if(i == age):
                tr=round(lp/20)  
                agecl=round(lp/20)    

    bmiinfo=""    
    #conditions
    print("Your body mass index is: ", bmi)
    if ( bmi < 16):
        bmiinfo="according to your BMI, you are Severely Underweight"
        clbmi=4
    elif ( bmi >= 16 and bmi < 18.5):
        bmiinfo="according to your BMI, you are Underweight"
        clbmi=3
    elif ( bmi >= 18.5 and bmi < 25):
        bmiinfo="according to your BMI, you are Healthy"
        clbmi=2
    elif ( bmi >= 25 and bmi < 30):
        bmiinfo="according to your BMI, you are Overweight"
        clbmi=1
    elif ( bmi >=30):
        bmiinfo="according to your BMI, you are Severely Overweight"
        clbmi=0

    
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.to_numpy()
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.to_numpy()
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.to_numpy()
    ti=(clbmi+agecl)/2
    
    ## K-Means Based  Dinner Food
    Datacalorie=DinnerfoodseparatedIDdata[1:,1:len(DinnerfoodseparatedIDdata)]
    kmeans = KMeans(k=3, max_iter=100)
    X = np.random.rand(*Datacalorie.shape)
    kmeans.fit(X)
    labels = kmeans.predict(X)
    XValu=np.arange(0,len(labels))
    dnrlbl=labels

    ## K-Means Based  lunch Food
    Datacalorie=LunchfoodseparatedIDdata[1:,1:len(LunchfoodseparatedIDdata)]
    kmeans = KMeans(k=3, max_iter=100)
    X = np.random.rand(*Datacalorie.shape)
    kmeans.fit(X)
    labels = kmeans.predict(X)
    XValu=np.arange(0,len(labels))
    lnchlbl=labels
   
    ## K-Means Based  breakfast Food
    Datacalorie=breakfastfoodseparatedIDdata[1:,1:len(breakfastfoodseparatedIDdata)]
    kmeans = KMeans(k=3, max_iter=100)
    X = np.random.rand(*Datacalorie.shape)
    kmeans.fit(X)
    labels = kmeans.predict(X)
    XValu=np.arange(0,len(labels))
    brklbl=labels
    
    inp=[]
    ## Reading of the Dataet
    datafin=pd.read_csv(os.path.join(BASE_DIR ,"static/data/nutrition_distriution.csv"))
    datafin.head(5)
   
    dataTog=datafin.T
    bmicls=[0,1,2,3,4]
    agecls=[0,1,2,3,4]
    weightlosscat = dataTog.iloc[[1,2,7,8]]
    weightlosscat=weightlosscat.T
    weightgaincat= dataTog.iloc[[0,1,2,3,4,7,9,10]]
    weightgaincat=weightgaincat.T
    healthycat = dataTog.iloc[[1,2,3,4,6,7,9]]
    healthycat=healthycat.T
    weightlosscatDdata=weightlosscat.to_numpy()
    weightgaincatDdata=weightgaincat.to_numpy()
    healthycatDdata=healthycat.to_numpy()
    weightlosscat=weightlosscatDdata[1:,0:len(weightlosscatDdata)]
    weightgaincat=weightgaincatDdata[1:,0:len(weightgaincatDdata)]
    healthycat=healthycatDdata[1:,0:len(healthycatDdata)]
    
    
    weightlossfin=np.zeros((len(weightlosscat)*5,6),dtype=np.float32)
    weightgainfin=np.zeros((len(weightgaincat)*5,10),dtype=np.float32)
    healthycatfin=np.zeros((len(healthycat)*5,9),dtype=np.float32)
    t=0
    r=0
    s=0
    yt=[]
    yr=[]
    ys=[]
    for zz in range(5):
        for jj in range(len(weightlosscat)):
            valloc=list(weightlosscat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightlossfin[t]=np.array(valloc)
            yt.append(brklbl[jj])
            t+=1
        for jj in range(len(weightgaincat)):
            valloc=list(weightgaincat[jj])
            #print (valloc)
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightgainfin[r]=np.array(valloc)
            yr.append(lnchlbl[jj])
            r+=1
        for jj in range(len(healthycat)):
            valloc=list(healthycat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            healthycatfin[s]=np.array(valloc)
            ys.append(dnrlbl[jj])
            s+=1

    X_test=np.zeros((len(healthycat)*5,9),dtype=np.float32)
    
    for jj in range(len(healthycat)):
        valloc=list(healthycat[jj])
        valloc.append(agecl)
        valloc.append(clbmi)
        X_test[jj]=np.array(valloc)*ti
    
    
    X_train=healthycatfin# Features
    y_train=ys # Labels
    
    #Create a Gaussian Classifier
    clf=RandomForestClassifier(n_estimators=100)
    
    #Train the model using the training sets y_pred=clf.predict(X_test)
    clf.fit(X_train,y_train)
    
    
    X_test2=X_test
    y_pred=clf.predict(X_test)
   
    
    returndata=[]
    for ii in range(len(y_pred)):
        print(y_pred)
        if y_pred[ii]==1:
            returndata.append(Food_itemsdata[ii])
            findata=Food_itemsdata[ii]
            
    returndata.append(bmi)
    returndata.append(bmiinfo)

    return returndata
