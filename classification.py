# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 12:27:22 2018

@author: DongliangLu
"""

import pandas as pd
import numpy as np
import pickle


from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import OneHotEncoder
from sklearn import metrics
from sklearn.model_selection import KFold 

from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import train_test_split,KFold
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.svm import LinearSVC,SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA


import seaborn as sns
#sns.pairplot(data,vars=["X1","X2"],hue="Y")


def get_set(X):
    return np.ones(X.shape) * (X!=0)

def get_idf(X_set):
    idf = np.sum(X_set, axis = 0)
    idf = np.log( (1+X_set.shape[0] ) / (1+idf) ) + 1
    return idf

def get_tfidf(X_set,idf):
    return X_set*idf

ML_data_save_basic_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\ML"
Y_save_add = ML_data_save_basic_add + "\\Y.pickle"
X_save_add = ML_data_save_basic_add + "\\X.pickle"

with open(Y_save_add,"rb") as f:
    tem=pickle.load(f, encoding='latin1')
Y=tem
with open(X_save_add,"rb") as f:
    tem=pickle.load(f, encoding='latin1')
X=tem

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

X_train_set =  get_set(X_train)
X_test_set =  get_set(X_test)
idf = get_idf(X_train_set)
X_train_tfidf = get_tfidf(X_train_set, idf)
X_test_tfidf = get_tfidf(X_test, idf)


#%% NB 
alpha=0.5
sk_model=MultinomialNB(alpha=alpha)
sk_model.fit(X_train,Y_train)
Y_train_pred=sk_model.predict(X_train)
print("MultinomialNB count train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test)
print("MultinomialNB count test accuracy:")
print(np.average(Y_test_pred==Y_test))


alpha=0.5
sk_model=MultinomialNB(alpha=alpha)
sk_model.fit(X_train_set,Y_train)
Y_train_pred=sk_model.predict(X_train_set)
print("MultinomialNB set train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test_set)
print("MultinomialNB set test accuracy:")
print(np.average(Y_test_pred==Y_test))


alpha=0.5
sk_model=MultinomialNB(alpha=alpha)
sk_model.fit(X_train_tfidf,Y_train)
Y_train_pred=sk_model.predict(X_train_tfidf)
print("MultinomialNB tfidf train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test_tfidf)
print("MultinomialNB tfidf test accuracy:")
print(np.average(Y_test_pred==Y_test))

sk_model=GaussianNB()
sk_model.fit(X_train_tfidf,Y_train)
Y_train_pred=sk_model.predict(X_train_tfidf)
print("GaussianNB tfidf train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test_tfidf)
print("GaussianNB tfidf test accuracy:")
print(np.average(Y_test_pred==Y_test))


'''
MultinomialNB count train accuracy:
0.851461038961039
MultinomialNB count test accuracy:
0.8025889967637541
MultinomialNB set train accuracy:
0.8766233766233766
MultinomialNB set test accuracy:
0.8058252427184466
MultinomialNB tfidf train accuracy:
0.9318181818181818
MultinomialNB tfidf test accuracy:
0.7766990291262136
GaussianNB tfidf train accuracy:
0.9358766233766234
GaussianNB tfidf test accuracy:
0.6957928802588996
'''

#%% KNeighbors
neighbor=2
sk_model=KNeighborsClassifier(n_neighbors=neighbor)
sk_model.fit(X_train,Y_train)
Y_train_pred=sk_model.predict(X_train)
print("KNeighbors count train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test)
print("KNeighbors count test accuracy:")
print(np.average(Y_test_pred==Y_test))


sk_model=KNeighborsClassifier(n_neighbors=neighbor)
sk_model.fit(X_train_set,Y_train)
Y_train_pred=sk_model.predict(X_train_set)
print("KNeighbors set train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test_set)
print("KNeighbors set test accuracy:")
print(np.average(Y_test_pred==Y_test))


sk_model=KNeighborsClassifier(n_neighbors=neighbor)
sk_model.fit(X_train_tfidf,Y_train)
Y_train_pred=sk_model.predict(X_train_tfidf)
print("KNeighbors tfidf train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test_tfidf)
print("KNeighbors tfidf test accuracy:")
print(np.average(Y_test_pred==Y_test))

#N=5
"""
KNeighbors count test accuracy:
0.7281553398058253

KNeighbors set test accuracy:
0.6472491909385113

KNeighbors tfidf test accuracy:
0.7087378640776699
KNeighbors tfidf test accuracy:
0.7087378640776699
"""
#N=3
'''
KNeighbors count test accuracy:
0.7378640776699029
KNeighbors set test accuracy:
0.6666666666666666
KNeighbors tfidf test accuracy:
0.6925566343042071
'''

#N=2
"""
KNeighbors count test accuracy:
0.7540453074433657
KNeighbors set test accuracy:
0.6925566343042071
KNeighbors tfidf test accuracy:
0.7152103559870551
"""





#%% LDA (slow)
sk_model=LDA()
sk_model.fit(X_train,Y_train)
Y_train_pred=sk_model.predict(X_train)
print("LDA count train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test)
print("LDA count test accuracy:")
print(np.average(Y_test_pred==Y_test))


sk_model=LDA()
sk_model.fit(X_train_set,Y_train)
Y_train_pred=sk_model.predict(X_train_set)
print("LDA set train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test_set)
print("LDA set test accuracy:")
print(np.average(Y_test_pred==Y_test))


sk_model=LDA()
sk_model.fit(X_train_tfidf,Y_train)
Y_train_pred=sk_model.predict(X_train_tfidf)
print("LDA tfidf train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test_tfidf)
print("LDA tfidf test accuracy:")
print(np.average(Y_test_pred==Y_test))

"""
LDA count train accuracy:
0.9456168831168831
LDA count test accuracy:
0.39158576051779936
LDA count train accuracy:
0.9431818181818182
LDA count test accuracy:
0.6699029126213593
LDA count train accuracy:
0.9431818181818182
LDA count test accuracy:
0.45307443365695793
"""



#%% QDA (very slow)
sk_model=QDA()
sk_model.fit(X_train,Y_train)
Y_train_pred=sk_model.predict(X_train)
print("QDA count train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test)
print("QDA count test accuracy:")
print(np.average(Y_test_pred==Y_test))


sk_model=QDA()
sk_model.fit(X_train_set,Y_train)
Y_train_pred=sk_model.predict(X_train_set)
print("QDA set train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test_set)
print("QDA set test accuracy:")
print(np.average(Y_test_pred==Y_test))


sk_model=QDA()
sk_model.fit(X_train_tfidf,Y_train)
Y_train_pred=sk_model.predict(X_train_tfidf)
print("QDA tfidf train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test_tfidf)
print("QDA tfidf test accuracy:")
print(np.average(Y_test_pred==Y_test))


"""
QDA count train accuracy:
0.9577922077922078
QDA count test accuracy:
0.22653721682847897
QDA count train accuracy:
0.0016233766233766235
QDA count test accuracy:
0.003236245954692557
QDA count train accuracy:
0.9586038961038961
QDA count test accuracy:
0.07119741100323625
"""
#%% Logistic (too slow I don't even want to wait)

sk_model=LogisticRegression(C=1e30, multi_class="multinomial",solver="sag")
sk_model.fit(X_train,Y_train)
Y_train_pred=sk_model.predict(X_train)
print("Logistic count train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test)
print("Logistic count test accuracy:")
print(np.average(Y_test_pred==Y_test))


sk_model=LogisticRegression(C=1e30, multi_class="multinomial",solver="sag")
sk_model.fit(X_train_set,Y_train)
Y_train_pred=sk_model.predict(X_train_set)
print("Logistic set train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test_set)
print("Logistic set test accuracy:")
print(np.average(Y_test_pred==Y_test))


sk_model=LogisticRegression(C=1e30, multi_class="multinomial",solver="sag")
sk_model.fit(X_train_tfidf,Y_train)
Y_train_pred=sk_model.predict(X_train_tfidf)
print("Logistic tfidf train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test_tfidf)
print("Logistic tfidf test accuracy:")
print(np.average(Y_test_pred==Y_test))


"""
0.806
0.770

"""

#%%

sk_model=LinearSVC(C=100,loss="hinge",multi_class="crammer_singer",tol=1e-9,max_iter=10000)
sk_model.fit(X_train,Y_train)
Y_train_pred=sk_model.predict(X_train)
print("Logistic count train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(X_test)
print("Logistic count test accuracy:")
print(np.average(Y_test_pred==Y_test))


#%% PCA to reduce dimension

#pca = PCA(0.9)
pca = PCA(0.95)
PCA_X_train = pca.fit_transform(X_train)
PCA_X_test = pca.transform(X_test)
print("dimension after PCA: %0.0d"%PCA_X_train.shape[1])
print("PCA components shape: (%0.0d, %0.0d) "%(pca.components_.shape[0], pca.components_.shape[1]))
print("PCA explained variance ratio: %0.2f%%" % (pca.explained_variance_ratio_.sum()*100)) 

PCA_X_train_set = pca.fit_transform(X_train_set)
PCA_X_test_set = pca.transform(X_test_set)

PCA_X_train_tfidf = pca.fit_transform(X_train_tfidf)
PCA_X_test_tfidf = pca.transform(X_test_tfidf)



#%% PCA data version

#%%

sk_model=GaussianNB()
sk_model.fit(PCA_X_train,Y_train)
Y_train_pred=sk_model.predict(PCA_X_train)
print("NB count train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(PCA_X_test)
print("NB count test accuracy:")
print(np.average(Y_test_pred==Y_test))



sk_model=GaussianNB()
sk_model.fit(PCA_X_train_set,Y_train)
Y_train_pred=sk_model.predict(PCA_X_train_set)
print("NB set train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(PCA_X_test_set)
print("NB set test accuracy:")
print(np.average(Y_test_pred==Y_test))



sk_model=GaussianNB()
sk_model.fit(PCA_X_train_tfidf,Y_train)
Y_train_pred=sk_model.predict(PCA_X_train_tfidf)
print("NB tfidf train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(PCA_X_test_tfidf)
print("NB tfidf test accuracy:")
print(np.average(Y_test_pred==Y_test))


"""
GaussianNB count train accuracy:
0.18993506493506493
GaussianNB count test accuracy:
0.1488673139158576
GaussianNB set train accuracy:
0.29545454545454547
GaussianNB set test accuracy:
0.1650485436893204
GaussianNB tfidf train accuracy:
0.2719155844155844
GaussianNB tfidf test accuracy:
0.3268608414239482
"""

#%%

sk_model=LDA()
sk_model.fit(PCA_X_train,Y_train)
Y_train_pred=sk_model.predict(PCA_X_train)
print("LDA count train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(PCA_X_test)
print("LDA count test accuracy:")
print(np.average(Y_test_pred==Y_test))


sk_model=LDA()
sk_model.fit(PCA_X_train_set,Y_train)
Y_train_pred=sk_model.predict(PCA_X_train_set)
print("LDA set train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(PCA_X_test_set)
print("LDA set test accuracy:")
print(np.average(Y_test_pred==Y_test))


sk_model=LDA()
sk_model.fit(PCA_X_train_tfidf,Y_train)
Y_train_pred=sk_model.predict(PCA_X_train_tfidf)
print("LDA tfidf train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(PCA_X_test_tfidf)
print("LDA tfidf test accuracy:")
print(np.average(Y_test_pred==Y_test))

"""
LDA count train accuracy:
0.46266233766233766
LDA count test accuracy:
0.47249190938511326
LDA set train accuracy:
0.8782467532467533
LDA set test accuracy:
0.8284789644012945
LDA tfidf train accuracy:
0.7962662337662337
LDA tfidf test accuracy:
0.7346278317152104
"""



#0.95
"""
LDA count train accuracy:
0.5056818181818182
LDA count test accuracy:
0.4919093851132686
LDA set train accuracy:
0.8928571428571429
LDA set test accuracy:
0.8317152103559871
LDA tfidf train accuracy:
0.8352272727272727
LDA tfidf test accuracy:
0.7281553398058253
"""


#%%

sk_model=QDA()
sk_model.fit(PCA_X_train,Y_train)
Y_train_pred=sk_model.predict(PCA_X_train)
print("QDA count train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(PCA_X_test)
print("QDA count test accuracy:")
print(np.average(Y_test_pred==Y_test))


sk_model=QDA()
sk_model.fit(PCA_X_train_set,Y_train)
Y_train_pred=sk_model.predict(PCA_X_train_set)
print("QDA set train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(PCA_X_test_set)
print("QDA set test accuracy:")
print(np.average(Y_test_pred==Y_test))


sk_model=QDA()
sk_model.fit(PCA_X_train_tfidf,Y_train)
Y_train_pred=sk_model.predict(PCA_X_train_tfidf)
print("QDA tfidf train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(PCA_X_test_tfidf)
print("QDA tfidf test accuracy:")
print(np.average(Y_test_pred==Y_test))

"""
QDA count train accuracy:
0.4407467532467532
QDA count test accuracy:
0.3365695792880259
QDA set train accuracy:
0.952922077922078
QDA set test accuracy:
0.49514563106796117
QDA tfidf train accuracy:
0.9594155844155844
QDA tfidf test accuracy:
0.39805825242718446
"""



#%%


sk_model=LogisticRegression(C=1e30, multi_class="multinomial",solver="sag")
sk_model.fit(PCA_X_train,Y_train)
Y_train_pred=sk_model.predict(PCA_X_train)
print("Logistic count train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(PCA_X_test)
print("Logistic count test accuracy:")
print(np.average(Y_test_pred==Y_test))


sk_model=LogisticRegression(C=1e30, multi_class="multinomial",solver="sag")
sk_model.fit(PCA_X_train_set,Y_train)
Y_train_pred=sk_model.predict(PCA_X_train_set)
print("Logistic set train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(PCA_X_test_set)
print("Logistic set test accuracy:")
print(np.average(Y_test_pred==Y_test))


sk_model=LogisticRegression(C=1e30, multi_class="multinomial",solver="sag")
sk_model.fit(PCA_X_train_tfidf,Y_train)
Y_train_pred=sk_model.predict(PCA_X_train_tfidf)
print("Logistic tfidf train accuracy:")
print(np.average(Y_train_pred==Y_train))
Y_test_pred=sk_model.predict(PCA_X_test_tfidf)
print("Logistic tfidf test accuracy:")
print(np.average(Y_test_pred==Y_test))

"""
Logistic count train accuracy:
0.5405844155844156
Logistic count test accuracy:
0.5339805825242718
Logistic set train accuracy:
0.9131493506493507
Logistic set test accuracy:
0.8381877022653722
Logistic tfidf train accuracy:
0.8563311688311688
Logistic tfidf test accuracy:
0.7928802588996764
"""


#0.95
"""
Logistic count train accuracy:
0.5698051948051948
Logistic count test accuracy:
0.5663430420711975
Logistic set train accuracy:
0.9172077922077922
Logistic set test accuracy:
0.8511326860841424
Logistic tfidf train accuracy:
0.8790584415584416
Logistic tfidf test accuracy:
0.8090614886731392
"""


#%% kneighbor

neighbors=3

for neighbors in range(1,6):
    
    print("neighbors: %0.0d"%neighbors)

    sk_model=KNeighborsClassifier(n_neighbors=neighbors)
    sk_model.fit(PCA_X_train,Y_train)
    Y_train_pred=sk_model.predict(PCA_X_train)
    print("K neighbor count train accuracy:")
    print(np.average(Y_train_pred==Y_train))
    Y_test_pred=sk_model.predict(PCA_X_test)
    print("K neighbor count test accuracy:")
    print(np.average(Y_test_pred==Y_test))
    
    
    sk_model=KNeighborsClassifier(n_neighbors=neighbors)
    sk_model.fit(PCA_X_train_set,Y_train)
    Y_train_pred=sk_model.predict(PCA_X_train_set)
    print("K neighbor set train accuracy:")
    print(np.average(Y_train_pred==Y_train))
    Y_test_pred=sk_model.predict(PCA_X_test_set)
    print("K neighbor set test accuracy:")
    print(np.average(Y_test_pred==Y_test))
    
    
    sk_model=KNeighborsClassifier(n_neighbors=neighbors)
    sk_model.fit(PCA_X_train_tfidf,Y_train)
    Y_train_pred=sk_model.predict(PCA_X_train_tfidf)
    print("K neighbor tfidf train accuracy:")
    print(np.average(Y_train_pred==Y_train))
    Y_test_pred=sk_model.predict(PCA_X_test_tfidf)
    print("K neighbor tfidf test accuracy:")
    print(np.average(Y_test_pred==Y_test))

#3
"""
K neighbor count train accuracy:
0.8555194805194806
QDA count test accuracy:
0.7249190938511327
K neighbor set train accuracy:
0.8676948051948052
K neighbor set test accuracy:
0.7799352750809061
K neighbor tfidf train accuracy:
0.8758116883116883
K neighbor tfidf test accuracy:
0.7961165048543689
"""






"""
neighbors: 1
K neighbor count train accuracy:
0.9650974025974026
QDA count test accuracy:
0.7605177993527508
K neighbor set train accuracy:
0.9983766233766234
K neighbor set test accuracy:
0.7928802588996764
K neighbor tfidf train accuracy:
0.9983766233766234
K neighbor tfidf test accuracy:
0.8187702265372169
neighbors: 2
K neighbor count train accuracy:
0.8920454545454546
QDA count test accuracy:
0.7313915857605178
K neighbor set train accuracy:
0.8863636363636364
K neighbor set test accuracy:
0.7669902912621359
K neighbor tfidf train accuracy:
0.898538961038961
K neighbor tfidf test accuracy:
0.8122977346278317
neighbors: 3
K neighbor count train accuracy:
0.8555194805194806
QDA count test accuracy:
0.7249190938511327
K neighbor set train accuracy:
0.8676948051948052
K neighbor set test accuracy:
0.7799352750809061
K neighbor tfidf train accuracy:
0.8758116883116883
K neighbor tfidf test accuracy:
0.7961165048543689
neighbors: 4
K neighbor count train accuracy:
0.838474025974026
QDA count test accuracy:
0.7313915857605178
K neighbor set train accuracy:
0.859577922077922
K neighbor set test accuracy:
0.7734627831715211
K neighbor tfidf train accuracy:
0.8717532467532467
K neighbor tfidf test accuracy:
0.7928802588996764
neighbors: 5
K neighbor count train accuracy:
0.8311688311688312
QDA count test accuracy:
0.7313915857605178
K neighbor set train accuracy:
0.8457792207792207
K neighbor set test accuracy:
0.7766990291262136
K neighbor tfidf train accuracy:
0.8579545454545454
K neighbor tfidf test accuracy:
0.8058252427184466
"""

























