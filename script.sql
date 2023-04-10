--------------------
------ PARTIE 1
--------------------

-- Script de Creation de base avec psql 

-- Supp base
DROP DATABASE IF EXISTS secu1 ;

-- Creation base
CREATE DATABASE secu1;
-- Connexion base
\c secu1;

-- Creation de la table
CREATE TABLE connexion (
  id serial primary key,
  name VARCHAR(100),
  password VARCHAR(100),
  email VARCHAR(100)
);

-- Insertion 
INSERT INTO connexion (name, password, email)
VALUES ('client', 'mdp', 'raphaguarim@gmail.com');

INSERT INTO connexion (name, password, email)
VALUES ('client2', 'f4f263e439cf40925e6a412387a9472a6773c2580212a4fb50d224d3a817de17', 'raphaguarim@gmail.com');

--------------------
------ PARTIE 2
--------------------

-- Creation de la table
CREATE TABLE commentaire (
  id integer REFERENCES connexion (id),
  content VARCHAR
);