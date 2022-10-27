import unittest

from main import IMDBDataManager 

# This is the class we want to test. So, we need to import it
class TestIMDBDataManager(unittest.TestCase):
    def setUp(self):
        self.num_movies = 10
        self.manager  = IMDBDataManager(self.num_movies)
        
    def test_scraper_data_correctness(self):
        url = 'https://www.imdb.com/chart/top/'
        self.manager.Scraper(url)
        self.assertEqual(self.manager.df_movies.shape[0], self.num_movies)
        for i in range(self.num_movies):
            self.assertGreater(len(self.manager.df_movies.loc[i, 'Title']),0)
            self.assertGreaterEqual(self.manager.df_movies.loc[i, 'Rating'],0)
            self.assertLessEqual(self.manager.df_movies.loc[i, 'Rating'],10)
            self.assertGreater(self.manager.df_movies.loc[i, 'Votes'],0)
            self.assertLess(self.manager.df_movies.loc[i, 'Oscars'],12)
  
    def test_scraper_url(self):        
        url = 'https://www.google.com/'
        self.assertRaises(ValueError, self.manager.Scraper, url)
        
    
        
    