## Hello DataPAO team 👋

### Let me introduce to you my take-home project: 
### The Big IMDB quest

A short recap of the given tasks:
- Implement **Data Scraper** which scrapes *Title, Rating, Number of votes and Number of Oscars* for each movie from the IMDB TOP250 list,
- Create two Rating Adjustment functions: 
    **Oscar Calculator** and **Review Penalizer** which modify the rating according to given conditions,
- Write out the TOP20 movies in a sorted way including both the original and the adjusted new ratings to a file.

### How to run the project
#### 1. Create a local copy of this repository
[The-Big-IMDB-quest](https://github.com/ollligator/The-Big-IMDB-quest.git)
#### 2. Open a terminal/console in the root folder of this project 
Ideally, the folder looks like this <br /><br />
<img src="/assets/folder.png" width="300">
#### 3. Run the command below to install the requirements
```
pip install -r requirements.txt
``` 

#### 4. Run the command below to scrape movies and recalculate their rating
```
python main.py
```
This is the console output after a perfect pass of all functions <br /><br />
<img src="/assets/result.png" width="500">
#### 5. Run the following command to perform the unit tests
```
python -m unittest discover -b
```
or you can use another one, but the output might be confusing <br />
```
python -m unittest discover -v
```
## Description 
Environment: **Spyder IDE** <br />
Language: **Python** <br />
Libraries:
- **pandas** for data manipulation
- **BeautifulSoup** and **requests** for web-page investigation 

Data was obtained from:
- [TOP250 itself](https://www.imdb.com/chart/top/)
- Movie awards pages like [The Godfather Awards](https://www.imdb.com/title/tt0068646/awards/?ref_=tt_awd)
 
To accomplish the task, I created two classes: Movie and IMDBDataManager. <br />
- Movie class is responsible for reading movie information from a movie list by index
- IMDBDataManager has 5 main functions: 
  - **Scraper()** creates a dataframe with a given number of films with 'Title', 'Rating', 'Votes', 'Oscars' attributes, 
  - **StoreTopMovies()** saves the original data into a csv file,
  - **ReviewPenalizer()** calculates rating review correction values and adds two attributes 'Rating_Review_Correction' and 'Rating_Review',
  - **OscarCalculator()** calculates rating Oscar correction values and adds two attributes 'Rating_Oscar_Correction' and 'Rating_Oscar',
  - **StoreNewRatings()** calculates new ratings considering Oscar and review corrections and saves updated values into a csv file.

#### The outcome of Scraper() and StoreTopMovies() is IMDBtopN_initial.csv file <br />
<img src="/assets/df.png" width="400"> <br />
#### The outcome of Scraper() and StoreTopMovies() is IMDBtopN_newrating.csv file <br />
<img src="/assets/new_df.png" width="900">

### Thank you for your attention! 🙌
