# Movie Wizard - Using Machine Learning to Generate Films Recommendations
Users spend 17.8 minutes on average searching for movies to watch on Netflix's
platform, and if the user has other platforms with more films and series available, the mean
searching time can be even more prominent. Additionally, movie platforms stopped showing
average ratings for their movies, undermining searches that take critics' and audience opinions
into consideration, leaving the user to resort to platforms that aggregate critics' scores, such as
Rotten Tomatoes and IMDB.
The team is creating an application that generates movie recommendations utilizing
machine learning unsupervised algorithms, data visualization, and user preferences as input to
address the problem. Apart from the personalized suggestions, this application provides the user
with analysis tools across various streaming platforms, genres, locality, and critics' opinions to
understand the statistics behind the film industry. Lastly, the application allows users to discover
more entertainment options and save time searching through massive film directories. 

## Data Dictionary
|Syntax|DataFrame|Description|Data Type|Example|
|:---|:---:|:----|:---:|:---:|
|title|movies_data|Movies' title|string|The Irishman|
|year|movies_data|Movies' lauch year|int64|2019|
|age|movies_data|Parental Guidance Minimal Age Suggested|string|18+|
|imdb|movies_data|IMDB Score|float64|7.8|
|rotten_tomatoes|movies_data|Rotten Tomato Score|float64|98.0|
|netflix|movies_data|Movie is available on Netflix|bool|True|
|hulu|movies_data|Movie is available on Hulu|bool|False|
|prime_video|movies_data|Movie is available on Prime Video|bool|False|
|disney|movies_data|Movie is available on Disney+|bool|False|
|directors|movies_data|Movie's directors|object(list)|[Marting Scorsese]|
|genres|movies_data|Movie's genres|object(list)|[Biography, Crime, Drama]|
|language|movies_data|Movie's original language|object(list)|[English, Italian, Latin, Spanish, German]|
|runtime|movies_data|Movie's length in minutes|float64|209.0|
|group|tsne_df|Movie's cluster number|object(int)|18|
|X|tsne_df|The X-value on the t-distributed stochastic neighbor embedding|object(float64)|-64.7094|
|Y|tsne_df|The Y-value on the t-distributed stochastic neighbor embedding|object(float64)|43.7906|
