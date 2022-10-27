#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests


def get_content(url, page_type):
    
    headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'Accept-Language': 'en-US',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    
    req = requests.get(url, headers)
    content = bs(req.content, page_type)
    
    return content


class Movie:
    movie_id = []
    title = []
    rating = 0
    votes = 0
    oscars = 0
    
    def __init__(self, movies, ind):
        

        
        
        self.set_title(movies, ind)
        self.set_rating(movies, ind)
        self.set_votes(movies, ind)
        self.set_oscars(movies, ind)
        

    def set_title(self, movies, ind):
        len_year = 7
        title_full = (' '.join(movies.select('.titleColumn')[ind].get_text().strip().split()).replace('.', ''))
        self.title = title_full[len(str(ind))+1:-len_year]
        
        if(len(self.title) == 0):
            print(f'Something went wrong with a title of the movie number {ind}')
        
    
    def set_rating(self, movies, ind):
        self.rating = float(movies.select('.ratingColumn.imdbRating')[ind].get_text().strip())
        
        if(self.rating > 10):
            print(f'Something went wrong with a rating value of the movie number {ind}')
    
    def set_votes(self, movies, ind):
        self.votes = int(movies.select('.posterColumn span[name=nv]')[ind].get('data-value'))
        
        if(self.votes == 0):
            print(f'Something went wrong with a number of votes for the movie number {ind}')
    
    def set_id(self, movies, ind):        
        self.movie_id = movies.find_all(class_='seen-widget')[ind].get('data-titleid')
        
        if(len(self.movie_id) == 0):
            print(f'Something went wrong with a link of the movie number {ind}')
    
    def set_oscars(self, movies, ind):
        self.set_id(movies, ind)
        
        award_url = 'https://www.imdb.com/title/' + self.movie_id +'/awards/?ref_=tt_awd/'
        award_content = get_content(award_url, 'lxml')
        for award in award_content.select('.awards'):
            aw = award.find(class_='title_award_outcome').get_text()
            if ("Winner" in aw) and ("Oscar" in aw):
                self.oscars = int(award.find(class_='title_award_outcome').get('rowspan')) 
        
        if(self.oscars > 12):
            print(f'Something went wrong with a number of oscars for the movie number {ind}')        
        
        
        

class IMDBDataManager:
    def __init__(self, num_movies):
        self.num_movies = num_movies
        self.df_movies = pd.DataFrame()
        
    def Scraper(self, url):
        cols = ['Title', 'Rating', 'Votes', 'Oscars']
        content = get_content(url, 'lxml')
        for movies in content.select('.lister-list'):
            for i in range(self.num_movies):
                mov = Movie(movies, i)
                data = [mov.title, 
                        mov.rating,
                        mov.votes,
                        mov.oscars]
                self.df_movies = self.df_movies.append(pd.Series(data, index=cols),ignore_index=True)
        if (self.df_movies.shape[0]!= self.num_movies):
            raise ValueError('The movies were not scraped correctly from the page, please check the link. A .csv file cannot be saved')
    
    def StoreTopMovies(self):    
        self.df_movies.to_csv('IMDBtop'+str(self.df_movies.shape[0])+'_initial.csv')
        
    def ReviewPenalizer(self):
        penalty_step = 100000
        deduction = 0.1
        max_votes = self.df_movies['Votes'].max()    
             
        self.df_movies['Rating_Review_Correction'] = round((max_votes - self.df_movies['Votes']) // penalty_step * deduction,3)
        self.df_movies['Rating_Review'] =  round(self.df_movies['Rating'] - self.df_movies['Rating_Review_Correction'],3) 
            
    def OscarCalculator(self):
        oscar_mapper = {0: 0, range(1,3): 0.3, range(3,6): 0.5, range(6,11): 1, range(11,100): 1.5}
        self.df_movies['Rating_Oscar_Correction']= round(self.df_movies['Oscars'].replace(oscar_mapper),3)
        self.df_movies['Rating_Oscar'] =  round(self.df_movies['Rating'] + self.df_movies['Rating_Oscar_Correction'],3)
        
    
    def StoreNewRatings(self):
        if(self.df_movies.shape[1]>7):
            self.df_movies['Rating_New'] = round(self.df_movies['Rating'] + self.df_movies['Rating_Oscar_Correction'] - self.df_movies['Rating_Review_Correction'],3)
            sorted_df = self.df_movies.sort_values(by=['Rating_New'], ascending=False, ignore_index=True)
            sorted_df.to_csv('IMDBtop'+str(self.df_movies.shape[0])+'_newrating.csv')
        else:
            print('Please, call the penalizer and the calculator before saving')
            
            


            
num_movies = 20     
top_url = 'https://www.imdb.com/chart/top/'

manager  = IMDBDataManager(num_movies)
manager.Scraper(top_url)
manager.StoreTopMovies()
manager.ReviewPenalizer()
manager.OscarCalculator()
manager.StoreNewRatings()

        

    
    
        
    
    
    
    

