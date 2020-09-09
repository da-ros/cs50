-- Both correct, the first for some reason outputs the correct result but sorted alphabetically, too

--SELECT name FROM people WHERE id IN(SELECT person_id FROM stars WHERE movie_id IN(SELECT movie_id FROM stars JOIN people ON stars.person_id=people.id WHERE name="Kevin Bacon" AND birth=1958)) EXCEPT SELECT name FROM people WHERE name="Kevin Bacon";

SELECT name FROM people WHERE id IN(SELECT person_id FROM stars WHERE movie_id IN(SELECT movie_id FROM stars JOIN people ON stars.person_id=people.id WHERE name="Kevin Bacon" AND birth=1958)) AND NOT name="Kevin Bacon";