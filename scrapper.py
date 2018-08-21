import requests
import os
from bs4 import BeautifulSoup

def doesFileExists(filePathAndName):
	return os.path.exists(filePathAndName)
if doesFileExists('./Movie_List.csv'):
	pass
else:
	open('Movie_List.csv','w')
if doesFileExists('./Movie_Watched.csv'):
	pass
else:
	open('Movie_Watched.csv','w')
if doesFileExists('./Failed_Movie.csv'):
	pass
else:
	open('Failed_Movie.csv','w')
	
def write_csv(movie_list,download_dir,param):
	csv = open(download_dir, param)
	for key in movie_list.keys():
		movie_name = key
		imdb_rating = movie_list[key]
		row = movie_name + "%" + str(imdb_rating) + "\n"
		csv.write(row)

page = requests.get('https://www.imdb.com/list/ls058409670/')
soup = BeautifulSoup(page.text,'html.parser')

movie_name_list = soup.find(class_='article listo')
movie_name_list_items = movie_name_list.find_all(class_='lister-item-header')
movie_name_rating_items = movie_name_list.find_all(class_ = 'ipl-rating-widget')

mv_with_rt = {}
for movie_name,movie_rating in zip(movie_name_list_items,movie_name_rating_items):
    names = movie_name.find('a').text
    rating = movie_rating.find(class_ = 'ipl-rating-star__rating').text
    mv_with_rt[str(names)] = float(rating)

movie_list = {}
sortedList=sorted(mv_with_rt.values(),reverse=True)
for sortedKey in sortedList:
    for key, value in mv_with_rt.items():
        if value==sortedKey:
            movie_list[key]=value


write_csv(movie_list,"Movie_List.csv","a")
