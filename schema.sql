CREATE DATABASE IF NOT EXISTS movielab;
USE movielab;

CREATE TABLE movies (
  movieID     INT AUTO_INCREMENT PRIMARY KEY,
  title       VARCHAR(100) NOT NULL,
  genre       VARCHAR(50),
  director    VARCHAR(100),
  releaseYear INT CHECK (releaseYear >= 1900)
);

CREATE TABLE ratings (
  ratingID  INT AUTO_INCREMENT PRIMARY KEY,
  movieID   INT NOT NULL,
  story     INT CHECK (story     BETWEEN 1 AND 10),
  acting    INT CHECK (acting    BETWEEN 1 AND 10),
  visual    INT CHECK (visual    BETWEEN 1 AND 10),
  sound     INT CHECK (sound     BETWEEN 1 AND 10),
  direction INT CHECK (direction BETWEEN 1 AND 10),
  rating    DECIMAL(3,1),
  FOREIGN KEY (movieID) REFERENCES movies(movieID) ON DELETE CASCADE
);

DELIMITER //
CREATE TRIGGER calc_rating BEFORE INSERT ON ratings
FOR EACH ROW
BEGIN
  SET NEW.rating = ROUND((NEW.story + NEW.acting + NEW.visual
                        + NEW.sound + NEW.direction) / 5, 1);
END//
DELIMITER ;

CREATE VIEW top_movies AS
SELECT m.movieID, m.title, m.genre,
       ROUND(AVG(r.rating),1) AS avg_rating,
       COUNT(r.ratingID)      AS votes
FROM movies m JOIN ratings r ON m.movieID = r.movieID
GROUP BY m.movieID, m.title, m.genre
ORDER BY avg_rating DESC;
