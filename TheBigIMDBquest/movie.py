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
