SELECT COUNT (movie_id) AS n FROM ratings WHERE rating = 10.0;

--Shows which ones are
--SELECT title FROM movies JOIN ratings ON movies.id = ratings.movie_id WHERE rating = 10;