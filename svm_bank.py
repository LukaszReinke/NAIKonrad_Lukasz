"""
authors: Konrad Chrzanowski, Łukasz Reinke
emails: s17404@pjwstk.edu.pl , s15037@pjwstk.edu.pl

Żeby uruchomić program trzeba zainstalować

pip install pandas
pip install -U scikit-learn

"""

from sklearn.model_selection import train_test_split
from sklearn import svm, metrics
from sklearn.preprocessing import LabelEncoder
import pandas as pd


# Zbiór danych klasyfikuje osoby opisane przez zestaw atrybutów jako dobre lub złe ryzyko kredytowe
# W linku jest zawarty opis bazy danych która zosatła użyta w tym przykładzie: https://www.openml.org/d/31

data_frame = pd.read_csv("dataset_31_credit-g.csv")
collumns_to_encode = ['checking_status',  'credit_history', 'purpose',
        'savings_status', 'employment',
       'installment_commitment', 'personal_status', 'other_parties',
       'property_magnitude', 'other_payment_plans',
       'housing', 'job', 'own_telephone',
       'foreign_worker', 'class'] 

le = LabelEncoder()
for col in collumns_to_encode:
    print(data_frame[col])
    data_frame[col] = le.fit_transform(data_frame[col])
    print(data_frame[col])
    
# bad -> 0; good -> 1
# Podzielenie danych na 3 części 2/3 danych służy do nauki AI, a 1/3 służy do sprawdzania/testowania.

X_train, X_test, y_train,y_test = train_test_split(data_frame.drop(["class"], axis=1), data_frame["class"], test_size=1 / 3)

# Klasyfikator csv
clf = svm.SVC(kernel='linear') # Linear Kernel
# Trenowanie za pomocą zestawów treningowych
clf.fit(X_train, y_train)
# Przewidywanie wyniku na testowym zestawie danych
y_pred = clf.predict(X_test)

# wyświetlenie 3 pierwszych przypadków

print("Dla danych:")
print(X_test.iloc()[0])
print("wynik:")
print(y_pred[0])
print("-"*48)
print("Dla danych")
print(X_test.iloc()[1])
print("wynik:")
print(y_pred[1])
print("-"*48)
print("Dla danych")
print(X_test.iloc()[2])
print("wynik:")
print(y_pred[2])
print("-"*48)

# wyświetlenie z jaką precyzją/pewnością zostało przewidziane ryzyko kredytowe
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))