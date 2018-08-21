from selenium import webdriver
from scrapper import *
import time
import csv

driver = webdriver.Firefox()
url_list = ["https://www7.fmovies.se","https://www4.1movies.se"]
movie_num = 0
site_num =  0
watched_movie = {}
failed_movie = {}
def remove_alertbox():
	try:
		alertObj = driver.switch_to.alert
		alertObj.accept()
	except:
		print("No alertbox")
def remove_popup():
	try:
		driver.switch_to.window(driver.window_handles[-1])
		driver.close()
		driver.switch_to.window(driver.window_handles[0])
	except:
		print("No Pop Up")
		"""
with open("Movie_List.csv","r") as watched_file:
	i = 0
	reader = csv.reader(watched_file, delimiter='%')
	for row in reader:
		print(row[0].strip())
		"""
while True:
	movie_name = list(movie_list.keys())[movie_num]
	print("Movie Trying "+ movie_name)
	with open("Movie_Watched.csv","r") as watched_file:
		print("Checking If Movie in watched list")
		reader = csv.reader(watched_file, delimiter='%')
		flag = 0
		for row in reader:
			if movie_name.strip() in row[0].strip():
				print("Movie Already In watched list")
				flag = 1
				break
	if flag == 1:
		movie_num = movie_num+1
		continue
	
	print("Movie not in watched list")
	with open("Failed_Movie.csv","r") as failed_file:
	    reader = csv.reader(failed_file, delimiter='%')
	    print("Checking if movie in failed list")
	    for row in reader:
	        if movie_name.strip() in row[0].strip():
	        	print("Movie already failed to find in : "+url_list[site_num])
	        	print("Better Try Later")
        		flag = 1
        		break
	if flag == 1:
		movie_num = movie_num+1
		continue

	else:
		print("Movie is not in Failed List")
		driver.get(url_list[site_num])
		element = driver.find_element_by_xpath("//*[@id='search']/form/input")
		element.send_keys(movie_name)
		search = driver.find_element_by_xpath("//*[@id='search']/form/button")
		search.click()
		remove_popup()
		new_url1 = driver.current_url
		driver.get(new_url1)
		result = driver.find_element_by_class_name('name').text
		if result == movie_name:
			print("Movie is in This site\nNow this movie will be played")
			rating = mv_with_rt[movie_name]
			watched_movie[movie_name] = rating
			write_csv(watched_movie,"Movie_Watched.csv","a")
			print("Movie added to watched list")
			driver.find_element_by_class_name('poster').click()
			remove_popup()
			new_url2 = driver.current_url
			driver.get(new_url2)
			remove_alertbox()
			remove_popup()
			driver.find_element_by_id('player').click()
			remove_alertbox()
			remove_popup()
			break
		else:
			print('Movie does not Contain in this site')
			rating = mv_with_rt[movie_name]
			failed_movie[movie_name] = rating
			write_csv(failed_movie,"Failed_Movie.csv","a")
			print("Movie added to failed list")
			movie_num = movie_num + 1