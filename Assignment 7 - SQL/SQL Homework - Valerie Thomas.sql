USE sakila;

-- 1a. Display the first and last names of all actors from the table actor.
Select first_name, last_name
FROM actor;

-- 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
SELECT LTRIM(CONCAT(first_name,' ',last_name)) AS actor_name FROM actor;

-- 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." 
-- What is one query would you use to obtain this information?
SELECT*FROM actor
WHERE first_name = "Joe";

-- 2b. Find all actors whose last name contain the letters GEN:
SELECT last_name
FROM actor
WHERE last_name LIKE "%GEN%";

-- 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
SELECT last_name, first_name
FROM actor
WHERE last_name LIKE "%LI%"
ORDER BY last_name, first_name;

-- 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
SELECT*FROM country;

SELECT country_id, country
FROM country
WHERE country IN ('Afghanistan', 'Bangladesh', 'China');

-- 3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, 
-- so create a column in the table actor named description and use the data type BLOB (Make sure to research the type BLOB, 
-- as the difference between it and VARCHAR are significant).
SELECT*FROM actor;

ALTER TABLE actor
ADD COLUMN description LONGBLOB after last_update;

-- 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the description column.
ALTER TABLE actor
DROP COLUMN description;

-- 4a. List the last names of actors, as well as how many actors have that last name.
SELECT last_name, COUNT(last_name)
FROM actor
GROUP BY last_name;

-- 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors.
SELECT last_name, COUNT(last_name)
FROM actor
GROUP BY last_name
HAVING Count(last_name) >1;

-- 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to fix the record.
SELECT actor_id, first_name, last_name
FROM actor
WHERE first_name = 'GROUCHO' AND last_name='Williams';

UPDATE actor
SET first_name = "HARPO"
where actor_id =172;

SELECT*FROM actor
WHERE actor_id = 172;

-- 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! 
-- In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.
UPDATE actor
SET first_name = "GROUCHO"
WHERE first_name = "HARPO";

-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
DESCRIBE sakila.address;

-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:
SELECT first_name, last_name, address
FROM staff
INNER JOIN address 
ON staff.address_id=address.address_id;

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.
SELECT first_name, SUM(amount)
FROM staff
INNER JOIN payment
USING (staff_id)
GROUP BY first_name;

-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.
SELECT title, COUNT(actor_id)
FROM film
INNER JOIN film_actor
USING(film_id)
GROUP BY(film_id);

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
SELECT film_id
FROM film
WHERE title="Hunchback Impossible";
-- film_id = 439

SELECT COUNT(film_id)
FROM inventory
WHERE film_id=439;

-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. 
-- List the customers alphabetically by last name:
SELECT*FROM payment;
SELECT*FROM customer;

SELECT first_name, last_name, SUM(amount) AS "Total Amount Paid"
FROM customer
INNER JOIN payment
USING(customer_id)
GROUP BY(customer_id)
ORDER BY(last_name);

-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with 
-- the letters K and Q have also soared in popularity. 
-- Use subqueries to display the titles of movies starting with the letters K and Q whose language is English. 
SELECT*FROM film;
SELECT*FROM language;
-- language_id = 1

SELECT *
	FROM film
	WHERE language_id IN
	(
		SELECT language_id
		FROM language
		WHERE language_id = 1
	);

-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.
SELECT first_name, last_name
FROM actor
WHERE actor_id IN
(
	SELECT actor_id
	FROM film_actor
	WHERE film_id IN
	(
		SELECT film_id
		FROM film
		WHERE title = "Alone Trip"
	)
);


-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all 
-- Canadian customers. Use joins to retrieve this information.
-- names and email = customer 
-- for country = from customer > address id, address > city id, city > country id, country = 20
SELECT first_name, last_name, email 
FROM customer
JOIN address ON (customer.address_id = address.address_id)
JOIN city ON (address.city_id=city.city_id)
JOIN country ON (city.country_id=country.country_id);

-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. 
-- Identify all movies categorized as family films.
SELECT title
FROM film
WHERE film_id IN
(
	SELECT film_id
    FROM film_category
    WHERE category_id IN
    (
		SELECT category_id
        FROM category
        WHERE category_id=8
	)
);

-- 7e. Display the most frequently rented movies in descending order.
SELECT title, COUNT(f.film_id) AS 'Most_Rented_Movies'
FROM  film f
JOIN inventory i ON (f.film_id= i.film_id)
JOIN rental r ON (i.inventory_id=r.inventory_id)
GROUP BY title ORDER BY Most_Rented_Movies DESC;

-- 7f. Write a query to display how much business, in dollars, each store brought in.
SELECT staff_id AS "Store", SUM(amount) AS "Business in $"
FROM payment
Group BY staff_id;


-- 7g. Write a query to display for each store its store ID, city, and country.
SELECT store_id, city, country FROM store
JOIN address ON (store.address_id=address.address_id)
JOIN city ON (address.city_id=city.city_id)
JOIN country ON (city.country_id=country.country_id);

-- 7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following tables: 
-- category, film_category, inventory, payment, and rental.)
SELECT name AS "Top Five Categories", SUM(amount) AS "Gross" 
FROM category c
JOIN film_category fc ON (c.category_id=fc.category_id)
JOIN inventory i ON (fc.film_id=i.film_id)
JOIN rental r ON (i.inventory_id=r.inventory_id)
JOIN payment p ON (r.rental_id=p.rental_id)
GROUP BY name ORDER BY Gross  LIMIT 5;


-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. /
-- Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.
CREATE VIEW Top_Five_Gross_Revenue AS
SELECT name AS "Top Five Categories", SUM(amount) AS "Gross" 
FROM category c
JOIN film_category fc ON (c.category_id=fc.category_id)
JOIN inventory i ON (fc.film_id=i.film_id)
JOIN rental r ON (i.inventory_id=r.inventory_id)
JOIN payment p ON (r.rental_id=p.rental_id)
GROUP BY name ORDER BY Gross  LIMIT 5;

-- 8b. How would you display the view that you created in 8a?
SELECT * 
FROM Top_Five_Gross_Revenue;


-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
DROP VIEW Top_Five_Gross_Revenue;
