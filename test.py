import unittest

from main import IMDBDataManager 

# This is the class we want to test. So, we need to import it
class TestIMDBDataManager(unittest.TestCase):
    def setUp(self):
        self.num_movies = 20
    
    '''
    Checks the correctness of the data:
            - the number of rows in a dataframe must be equal to the number of movies
            - movie title must be at least 1 character
            - movie rating must be in [0, 10] interval
            - movie must have at least 1 vote
            - oscar number must be in [0, 12) interval (the record of Oscar is 11)
    '''    
    def test_scraper_data_correctness(self):
        url = 'https://www.imdb.com/chart/top/'
        manager  = IMDBDataManager(self.num_movies)
        manager.Scraper(url)
        self.assertEqual(manager.df_movies.shape[0], self.num_movies)
        for i in range(self.num_movies):
            self.assertGreater(len(manager.df_movies.loc[i, 'Title']),0)
            self.assertGreaterEqual(manager.df_movies.loc[i, 'Rating'],0)
            self.assertLessEqual(manager.df_movies.loc[i, 'Rating'],10)
            self.assertGreater(manager.df_movies.loc[i, 'Votes'],0)
            self.assertLess(manager.df_movies.loc[i, 'Oscars'],12)
    
    
    '''
    Checks the error in case of a wrong link
    '''
    def test_scraper_url(self):        
        url = 'https://www.google.com/'
        manager  = IMDBDataManager(self.num_movies)
        self.assertRaises(ValueError, manager.Scraper, url)
           
    
    '''
    Assigns 0 value to the number of oscars and checks if it doesn't affect the rating 
    '''
    
    def test_oscar_zero(self):       
        url = 'https://www.imdb.com/chart/top/'
        manager  = IMDBDataManager(self.num_movies)
        manager.Scraper(url)
        manager.df_movies.loc[0, 'Oscars'] = 0
        manager.OscarCalculator()
        self.assertEqual(manager.df_movies['Rating_Oscar'][0], manager.df_movies['Rating'][0])
    
    
    '''
    Checks if all the oscar corrections are in the [0, 1.5] interval
    '''    
    def test_oscar_rating_ranges(self):
        url = 'https://www.imdb.com/chart/top/'
        manager  = IMDBDataManager(self.num_movies)
        manager.Scraper(url)
        manager.OscarCalculator()
        for i in range(self.num_movies):
            self.assertGreaterEqual(manager.df_movies.loc[i, 'Rating_Oscar_Correction'],0)
            self.assertLessEqual(manager.df_movies.loc[i, 'Rating_Oscar_Correction'],1.5)
    
    '''
    Assigns 0 and 100 million (supposed to became max) values to the number of votes 
    and checks the correction value for the movie with 0 votes
    '''        
    def test_penalizer_min_max(self):       
        url = 'https://www.imdb.com/chart/top/'
        manager  = IMDBDataManager(self.num_movies)
        manager.Scraper(url)   
        manager.df_movies.loc[0, 'Votes'] = 0
        manager.df_movies.loc[self.num_movies-1, 'Votes'] = 100000000
        manager.ReviewPenalizer()
        self.assertEqual(manager.df_movies['Rating_Review_Correction'][0], 0.1*100000000 // 100000)
    
    '''
    Checks if all the penalizer corrections are in the [0, 10] interval
    '''     
    def test_penalizer_rating_ranges(self):
        url = 'https://www.imdb.com/chart/top/'
        manager  = IMDBDataManager(self.num_movies)
        manager.Scraper(url)
        manager.ReviewPenalizer()
        
        for i in range(self.num_movies):
            self.assertGreaterEqual(manager.df_movies.loc[i, 'Rating_Review_Correction'],0)
            self.assertLessEqual(manager.df_movies.loc[i, 'Rating_Review_Correction'],10)
    
    '''
    Checks if the final dataframe was sorted correctly 
    '''             
    def test_sorted_final_rating(self):
        url = 'https://www.imdb.com/chart/top/'
        manager  = IMDBDataManager(self.num_movies)
        manager.Scraper(url)
        manager.OscarCalculator()
        manager.ReviewPenalizer()
        manager.StoreNewRatings()
        self.assertGreaterEqual(manager.df_movies.loc[0, 'Rating_New'],manager.df_movies.loc[self.num_movies-1, 'Rating_New'])
        
            
    
        
    