from TheBigIMDBquest.imdbmanager import IMDBDataManager        
import sys
        
if __name__ == '__main__':            
    sys.path.append('../TheBigIMDBquest')
    num_movies = 20 
    print(f'Let\'s scrape {num_movies} movies from TOP250 IMDB')    
    top_url = 'https://www.imdb.com/chart/top/'    
    manager  = IMDBDataManager(num_movies)
    manager.Scraper(top_url)
    manager.StoreTopMovies()
    print('Review Penalizer and Oscar Calculator have started their job...')
    manager.ReviewPenalizer()
    manager.OscarCalculator()
    manager.StoreNewRatings()
