CREATE DATABASE IF NOT EXISTS db;
USE db;

CREATE TABLE IF NOT EXISTS User(
    UID int PRIMARY KEY,
    password varchar(255) NOT NULL,
    name varchar(255) NOT NULL,
    phone_number int NOT NULL,
    CHECK (phone_number > 5000000000)
);

CREATE TABLE IF NOT EXISTS Doctor(
    UID int PRIMARY KEY,
    diploma_registration_number int NOT NUll UNIQUE,
    FOREIGN KEY (UID) REFERENCES User(UID)
);