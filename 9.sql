-- According to staff results but this shows people repeated for several starrings
SELECT name FROM people WHERE id IN(SELECT person_id FROM stars JOIN movies ON stars.movie_id = movies.id WHERE year = 2004) ORDER BY birth;

-- Shows number of starrings in a 2004 movie for each actor
--SELECT name, birth, COUNT(name) AS n FROM people WHERE id IN(SELECT person_id FROM stars JOIN movies ON stars.movie_id = movies.id WHERE year = 2004) GROUP BY name ORDER BY n DESC;

-- Final real solution, not according to staff's solution
--SELECT name, COUNT(name) FROM people WHERE id IN(SELECT person_id FROM stars JOIN movies ON stars.movie_id = movies.id WHERE year = 2004) GROUP BY name ORDER BY birth;