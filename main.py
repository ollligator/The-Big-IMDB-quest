#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import re
from bs4 import BeautifulSoup as bs
import requests
import csv


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
    def __init__(self, movie, i):
        
        self.i = i
        self.movie_id = []
        self.title = []
        self.rating = 0
        self.votes = 0
        self.oscars = 0
        
        self.set_id(movie)
        self.set_title(movie)
        self.set_rating(movie)
        self.set_votes(movie)
        self.set_oscars(movie)
        

    def set_title(self, movie):
        len_year = 7
        title_full = (' '.join(movie.select('.titleColumn')[self.i].get_text().strip().split()).replace('.', ''))
        self.title = title_full[len(str(self.i))+1:-len_year]
    
    def set_rating(self, movie):
        self.rating = float(movie.select('.ratingColumn.imdbRating')[self.i].get_text().strip())
    
    def set_votes(self, movie):
        self.votes = int(movie.select('.posterColumn span[name=nv]')[self.i].get('data-value'))
    
    def set_id(self, movie):        
        self.movie_id = movie.find_all(class_='seen-widget')[self.i].get('data-titleid')
    
    def set_oscars(self, movie):
        
        oscars = 0;
        award_url = 'https://www.imdb.com/title/' + self.movie_id +'/awards/?ref_=tt_awd/'
        award_content = get_content(award_url, 'lxml')
        for award in award_content.select('.awards'):
            aw = award.find(class_='title_award_outcome').get_text()
            if ("Winner" in aw) and ("Oscar" in aw):
                oscars = award.find(class_='title_award_outcome').get('rowspan')        
        self.oscars = oscars

class Scraper:
    def __init__(self, num_movies):
        self.num_movies = num_movies
        self.movie_list = []
        
    def get_data(self, url):
        content = get_content(url, 'lxml')
        for movie in content.select('.lister-list'):
            for i in range(self.num_movies):
                mov = Movie(movie, i)
                self.movie_list.append(mov)
            
    def create_csv(self):
        with open('top250.csv', 'w',) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title', 'Rating', 'Votes', 'Oscars'])
            for movie in self.movie_list:
                writer.writerow([movie.title, 
                                 movie.rating,
                                 movie.votes,
                                 movie.oscars]) 
        
def ReviewPenalizer(movie_list):
    max_votes = max([movie.votes for movie in movie_list])
    penalty_step = 100000
    deduction = 0.1
    for movie in movie_list:
        penalty = (max_votes - movie.votes) // penalty_step
        print(penalty* deduction)
            
num_movies = 10     
top_url = 'https://www.imdb.com/chart/top/'

scraper = Scraper(num_movies)
scraper.get_data(top_url)
#scraper.create_csv()
ReviewPenalizer(scraper.movie_list)

        

    
    
        
    
    
    
    

