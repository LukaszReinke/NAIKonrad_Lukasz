import csv
import os

userDict = {}
##parser zostal przygotowany specjalnie dla naszego pliku
#dane zostaly przerobione recznie, seriale maja znaczek "$" zeby scraper mogl zalapac inny html
#dane zostaly przetlumacznone na jezyk angielski ze wzgledu na to ze uzywamy rottentomatos.com to zberania informacji o filmach/serialach
class MovieInfo():
    def __init__(self, movieName, movieScore, isMovie):
        self.movieName = movieName
        self.movieScore = movieScore
        self.isMovie = isMovie

with open("movieData.csv") as fp:
    reader = csv.reader(fp, delimiter=";", quotechar='"')
    data_read = [row for row in reader]
    

for idxRow, row in enumerate(data_read):
    if(idxRow == 0):
        continue
    userName = ""
    movieName = ""
    movieScore = ""
    for idxInnerRow, innerRow in enumerate(row):
        if (idxInnerRow == 0):
            continue
        if (idxInnerRow == 1):
            userName = innerRow
            userDict[innerRow] = []
            continue
        if (idxInnerRow != 1 & idxInnerRow % 2 == 0):
            movieName = innerRow            
        if (idxInnerRow != 1 & idxInnerRow % 2 == 1):
            movieScore = innerRow
            #jak ktos dal za malo filmow to nie dodajemy pustych pol do naszego zestawu danych
            if movieScore and movieName:
                #jak ktos wpisal 7.5 to kochany excel przerabial to na 7.maj :)
                userDict[userName].append(MovieInfo(movieName=movieName, movieScore= float(movieScore.replace(".maj", ".5")), isMovie=True))

#tutaj jest kulawy parser do .json, bo pythonowy nie chcial dzialac
file = open('dataset.json', 'x')
file.write("{")
for key, values in userDict.items():
    file.write(f'"{key}":')  
    file.write("{") 
    for indValue, value in enumerate(values):
        if (indValue == len(values) -1):
            file.write(f'"{value.movieName}" : {value.movieScore}')
            file.write("},")
        else:
            file.write(f'"{value.movieName}" : {value.movieScore},')
file.seek(file.tell() - 1, os.SEEK_SET)
file.write('')
file.write("}")
    
        
        



            

