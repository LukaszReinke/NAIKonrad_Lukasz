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

# Zbiór danych klasyfikuje pojazdy opisane przez zbiór parametrów jako VAN, SAAB, BUS i OPEL
# W linku jest zawarty opis bazy danych która zosatła użyta w tym przykładzie: https://www.openml.org/d/54

data_frame = pd.read_csv("dataset_54_vehicle.csv")
collumns_to_encode = []  
le = LabelEncoder()
data_frame['Class'] = le.fit_transform(data_frame['Class'])

# van -> 3, saab -> 2, bus -> 0, opel -> 1
# Podzielenie danych na 3 części 2/3 danych służy do nauki AI, a 1/3 służy do sprawdzania/testowania.

X_train, X_test, y_train,y_test = train_test_split(data_frame.drop(["Class"], axis=1), data_frame["Class"], test_size=1 / 3)
# Klasyfikator csv
clf = svm.SVC(kernel='linear') # Linear Kernel
# Trenowanie za pomocą zestawów treningowych
clf.fit(X_train, y_train)
# Przewidywanie wyniku na testowym zestawie danych
y_pred = clf.predict(X_test)

# wyświetlenie 3 pierwszych przypadków

print("Dla danych")
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

# wyświetlenie z jaką precyzją/pewnością został przewidziany rodzaj pojazdu.
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

