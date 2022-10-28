from .movie import Movie, get_content
from .fun import emoji
import pandas as pd

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
                print(f'{emoji()}  "{mov.title}" has been scrapped')
                data = [mov.title, 
                        mov.rating,
                        mov.votes,
                        mov.oscars]
                self.df_movies = self.df_movies.append(pd.Series(data, index=cols),ignore_index=True)
        if (self.df_movies.shape[0]!= self.num_movies):
            raise ValueError('The movies were not scraped correctly from the page, please check the link. A .csv file cannot be saved')
            
    def StoreTopMovies(self):    
        csv_name = 'IMDBtop'+str(self.df_movies.shape[0])+'_initial.csv'
        self.df_movies.to_csv(csv_name)
        print(f'You can find {csv_name} file in the folder')
    
        
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
            csv_name = 'IMDBtop'+str(self.df_movies.shape[0])+'_newrating.csv'
            sorted_df.to_csv(csv_name)
            print(f'All the ratings were successfully recalculated.\nYou can find {csv_name} file in the folder')
        else:
            print('Please, call the penalizer and the calculator before saving')
            
