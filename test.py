import unittest

from main import IMDBDataManager 

# This is the class we want to test. So, we need to import it
class TestIMDBDataManager(unittest.TestCase):
    def setUp(self):
        self.num_movies = 2

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
  
    def test_scraper_url(self):        
        url = 'https://www.google.com/'
        manager  = IMDBDataManager(self.num_movies)
        self.assertRaises(ValueError, manager.Scraper, url)
    
    def test_oscar_zero(self):       
        url = 'https://www.imdb.com/chart/top/'
        manager  = IMDBDataManager(self.num_movies)
        manager.Scraper(url)
        manager.df_movies.loc[0, 'Oscars'] = 0
        manager.OscarCalculator()
        self.assertEqual(manager.df_movies['Rating_Oscar'][0], manager.df_movies['Rating'][0])
        
    def test_oscar_rating_ranges(self):
        url = 'https://www.imdb.com/chart/top/'
        manager  = IMDBDataManager(self.num_movies)
        manager.Scraper(url)
        manager.OscarCalculator()
        for i in range(self.num_movies):
            self.assertGreaterEqual(manager.df_movies.loc[i, 'Rating_Oscar_Correction'],0)
            self.assertLessEqual(manager.df_movies.loc[i, 'Rating_Oscar_Correction'],1.5)
            
    
        
    