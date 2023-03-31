-- Script de Creation de base avec Postgresql

-- Creation base
CREATE DATABASE secu1;
-- Connexion base
\c secu1;

-- Creation de la table
CREATE TABLE connexion (
  name VARCHAR(100),
  password VARCHAR(100),
  email VARCHAR(100)
);

-- Insertion 
INSERT INTO connexion (name, password, email)
VALUES ('client', 'mdp', 'raphaguarim@gmail.com');

INSERT INTO connexion (name, password, email)
VALUES ('client2', 'f4f263e439cf40925e6a412387a9472a6773c2580212a4fb50d224d3a817de17', 'raphaguarim@gmail.com');


