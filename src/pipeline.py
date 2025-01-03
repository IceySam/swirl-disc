import random
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

class Pipeline:
    def __init__(self):
        pass
    
     # build model
    def build_model(self, vector, labels):
        log_model = LogisticRegression()

        X_train, X_test, y_train, y_test = train_test_split(vector, labels, test_size=0.2, random_state=42)
        
        log_model = log_model.fit(X=X_train, y=y_train)
        
        y_pred = log_model.predict(X_test)
        
        j = random.randint(0,len(X_test)-7)
        for i in range(j,j+7):
            print(y_pred[0])
            ind = vector.tolist().index(X_test[i].tolist())
            print(vector[ind].strip())
            
        print(accuracy_score(y_test, y_pred))