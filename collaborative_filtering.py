"""
authors: Konrad Chrzanowski, Łukasz Reinke
emails: s17404@pjwstk.edu.pl , s15037@pjwstk.edu.pl

Żeby uruchomić program trzeba zainstalować

pip install bs4
pip install numpy
pip install scipy
pip install scikit-learn
pip install urllib3
"""

import json
import numpy as np
from scraper import GetMovies

from compute_scores import cosing_score, euclidean_score

#implementacjia obu funkcji wyglada podobnie
# Finds users in the dataset that are similar to the input user 
def find_similar_users(dataset, user, num_users):
    if user not in dataset:
        raise TypeError('Cannot find ' + user + ' in the dataset')

    # Compute Pearson score between input user 
    # and all the users in the dataset
    scores = np.array([[x, euclidean_score(dataset, user, 
            x)] for x in dataset if x != user])

    # Sort the scores in decreasing order
    scores_sorted_desc = np.argsort(scores[:, 1])[::-1]
    scores_sorted_asc = np.argsort(scores[:, 1])[::1]

    # Extract the top 'num_users' scores
    top_users = scores_sorted_desc[:num_users]
    bottom_users =  scores_sorted_asc[:num_users]
    scores_both = {} 
    scores_both["top_users"] = scores[top_users]
    scores_both["bottom_users"] = scores[bottom_users]
    return scores_both

# Finds users in the dataset that are similar to the input user 
def find_similar_users_cosin(dataset, user, num_users):
    if user not in dataset:
        raise TypeError('Cannot find ' + user + ' in the dataset')

    # Compute Pearson score between input user 
    # and all the users in the dataset
    scores = np.array([[x, cosing_score(dataset, user, 
            x)] for x in dataset if x != user])

    # Sort the scores in decreasing order
    scores_sorted_desc = np.argsort(scores[:, 1])[::-1]
    scores_sorted_asc = np.argsort(scores[:, 1])[::1]

    # Extract the top 'num_users' scores
    top_users = scores_sorted_desc[:num_users]
    bottom_users =  scores_sorted_asc[:num_users]
    scores_both = {} 
    scores_both["top_users"] = scores[top_users]
    scores_both["bottom_users"] = scores[bottom_users]
    return scores_both

if __name__=='__main__':
    ratings_file = 'dataset.json'
    with open(ratings_file, 'r') as f:
        data = json.loads(f.read())

    user = input("Input user: ")
    
    #nadrostek "eu" to swiadczy o sposobie euklidesowym a "cos" o cosinusowym
    print('\nUsers similar to ' + user + ':\n')
    result_users = find_similar_users(data, user, 5) 
    result_users2 = find_similar_users_cosin(data,user,5)
    similar_users_eu = result_users["top_users"]
    unsimilar_users_eu = result_users["bottom_users"]
    similar_users_cos = result_users2["top_users"]
    unsimilar_users_cos = result_users2["bottom_users"]
    
    print('User\t\t\tSimilarity score euclidean')
    print('-'*41)
    for item in similar_users_eu:
        print(item[0], '\t\t', round(float(item[1]), 2))
     
    print('-'*41)   
    print('User\t\t\tUnsimilarity score euclidean')
    print('-'*41)
    for item in unsimilar_users_eu:
        print(item[0], '\t\t', round(float(item[1]), 2))
        
    print('User\t\t\tSimilarity score cos')
    print('-'*41)
    for item in similar_users_cos:
        print(item[0], '\t\t', round(float(item[1]), 2))
     
    print('-'*41)   
    print('User\t\t\tUnsimilarity score cos')
    print('-'*41)
    for item in unsimilar_users_cos:
        print(item[0], '\t\t', round(float(item[1]), 2))

    #chcemy dostac filmy ktorych nie ogladal wybrany uzytkownik
    movies_of_similar_user_eu = data[similar_users_eu[0][0]]
    movies_of_similar_user_cos = data[similar_users_cos[0][0]]
    movies_of_user = data[user]    
    
    #usun filmy ktore widzial drugi uzytkownik
    #z obu slownikow
    for item in movies_of_user:
        if item in movies_of_similar_user_eu:
            movies_of_similar_user_eu.pop(item)
        if item in movies_of_similar_user_cos:
            movies_of_similar_user_cos.pop(item)
    #posortuj filmy po ocenie
    sorted_movies_of_similar_user_eu = sorted(movies_of_similar_user_eu.items(), key=lambda x: x[1])
    sorted_movies_of_similar_user_cos = sorted(movies_of_similar_user_cos.items(), key=lambda x: x[1])
    #znajdz 5 filmow do polecenia i 5 filmow nie do polecenia
    top_5_to_recomend_eu = sorted_movies_of_similar_user_eu[-5:]
    bottom_5_to_recomend_eu = sorted_movies_of_similar_user_eu[:5]
    
    top_5_to_recomend_cos = sorted_movies_of_similar_user_cos[-5:]
    bottom_5_to_recomend_cos = sorted_movies_of_similar_user_cos[:5]
    
    #uzyj scrapera do wyswietlenia informacji o poleconych filmach
    for movie in top_5_to_recomend_eu:
        movies_dict = GetMovies(movie[0])
        print(f"Info for {movie[0]} : ")
        for key, value in movies_dict.items():
            print(f"\t\t{key} : {value}")
            
    print('-'*41)
    for movie in bottom_5_to_recomend_eu:
        movies_dict = GetMovies(movie[0])
        print(f"Info for {movie[0]} : ")
        for key, value in movies_dict.items():
            print(f"\t\t{key} : {value}")
    print('-'*41)   
    for movie in top_5_to_recomend_cos:
        movies_dict = GetMovies(movie[0])
        print(f"Info for {movie[0]} : ")
        for key, value in movies_dict.items():
            print(f"\t\t{key} : {value}")
    print('-'*41)   
    for movie in bottom_5_to_recomend_cos:
        movies_dict = GetMovies(movie[0])
        print(f"Info for {movie[0]} : ")
        for key, value in movies_dict.items():
            print(f"\t\t{key} : {value}")
    print('-'*41)
    
    
    
        

