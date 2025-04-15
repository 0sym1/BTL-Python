from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
import pandas as pd

data=pd.read_csv('processed.csv')

data.head()

y=data['strength'].values
x=data[['length','capital','small','special','numeric']].values

x.shape

xtrain,xtest,ytrain,ytest=tts(x,y,test_size=0.2,random_state=42)
print(xtrain.shape,ytrain.shape)
print(xtest.shape,ytest.shape)

sc=StandardScaler()
xtrain=sc.fit_transform(xtrain)
xtest=sc.transform(xtest)

model=MLPClassifier(hidden_layer_sizes=(16,16),max_iter=300)
model.fit(xtrain,ytrain)

ypred=model.predict(xtest)

print("The accuracy of the model is: ",accuracy_score(ytest,ypred)*100," % !!!")

print(classification_report(ytest,ypred))

print("The confusion matrix is: ")
cf=confusion_matrix(ytest,ypred)
print(cf)

# import joblib
# joblib.dump(sc,'scaler.pkl')
# joblib.dump(model,'model.pkl')

import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(15,10))
sns.heatmap(cf,annot=True,cmap='Blues')
plt.title('Confusion Matrix')
plt.savefig('confusion.jpg')
plt.show()