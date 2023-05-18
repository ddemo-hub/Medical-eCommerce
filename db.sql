CREATE DATABASE IF NOT EXISTS db;
USE db;

CREATE TABLE IF NOT EXISTS User(
    UID int PRIMARY KEY,
    password varchar(255) NOT NULL,
    name varchar(255) NOT NULL,
    phone_number bigint NOT NULL,
    CHECK (phone_number > 5000000000)
);

CREATE TABLE IF NOT EXISTS Doctor(
    UID int PRIMARY KEY,
    diploma_registration_number int NOT NUll UNIQUE,
    FOREIGN KEY (UID) REFERENCES User(UID)
);

CREATE TABLE IF NOT EXISTS Patient(
    UID int PRIMARY KEY,
    wallet_balance int NOT NULL DEFAULT 0,
    address varchar(255) NOT NULL,
    birthday datetime,
    allow_notifications int NOT NULL DEFAULT 1,
    CHECK (wallet_balance >= 0),
    FOREIGN KEY (UID) REFERENCES User(UID)
);

CREATE TABLE IF NOT EXISTS Pharmacy(
    UID int PRIMARY KEY,
    address varchar(255) NOT NULL,
    working_hours varchar(255),
    is_on_night_duty int,
    FOREIGN KEY (UID) REFERENCES User(UID)
);

CREATE TABLE IF NOT EXISTS Role(
    UID int,
    role varchar(255)NOT NULL,
    CHECK (role IN ('Patient', 'Doctor', 'Pharmacy')),
    FOREIGN KEY (UID) REFERENCES User(UID)
);

CREATE TABLE IF NOT EXISTS Rates(
    patient_id int,
    pharmacy_id int,
    rate double(2,1) NOT NULL DEFAULT 0.0,
    PRIMARY KEY(patient_id, pharmacy_id),
    FOREIGN KEY (patient_id) REFERENCES Patient(UID),
    FOREIGN KEY (pharmacy_id) REFERENCES Pharmacy(UID)
);

CREATE TABLE IF NOT EXISTS Drug_Order(
    order_id int PRIMARY KEY,
    date datetime NOT NULL,
    payment_method varchar(255) NOT NULL,
    total_price int NOT NULL,
    order_status varchar(255) NOT NULL,
    patient_id int NOT NULL,
    pharmacy_id int NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient(UID),
    FOREIGN KEY (pharmacy_id) REFERENCES Pharmacy(UID)
);

CREATE TABLE IF NOT EXISTS Prescription(
    prescription_id int PRIMARY KEY AUTO_INCREMENT,
    expiration_date datetime NOT NULL,
    order_id int,
    is_valid int NOT NULL,
    doctors_notes varchar(255),
    patient_id int NOT NULL, 
    FOREIGN KEY (order_id) REFERENCES Drug_Order(order_id),
    FOREIGN KEY (patient_id) REFERENCES Patient(UID)
);

CREATE TABLE IF NOT EXISTS Doctor_Prescribes_Prescription(
    doctor_id int,
    prescription_id int,
    FOREIGN KEY (doctor_id) REFERENCES Doctor(UID),
    FOREIGN KEY (prescription_id) REFERENCES Prescription(prescription_id),
    PRIMARY KEY(doctor_id, prescription_id)
);

CREATE TABLE IF NOT EXISTS Drug(
    drug_id int PRIMARY KEY AUTO_INCREMENT,
    drug_name varchar(255) NOT NULL,
    company varchar(255) NOT NULL,
    is_restricted int NOT NULL,
    price int NOT NULL,
    production_year int NOT NULL,
    drug_class varchar(255) NOT NULL,
    drug_info varchar(255) NOT NULL,
    use_count int NOT NULL,
    CHECK(price > 0)
);

CREATE TABLE IF NOT EXISTS Drug_In_Prescription(
    prescription_id int,
    drug_id int,
    count int NOT NULL DEFAULT 1,
    FOREIGN KEY (prescription_id) REFERENCES Prescription(prescription_id),
    FOREIGN KEY (drug_id) REFERENCES Drug(drug_id),
    PRIMARY KEY (prescription_id, drug_id),
    CHECK(count > 0)
);

CREATE TABLE IF NOT EXISTS Inventory(
    serial_number int NOT NULL UNIQUE AUTO_INCREMENT,
    pharmacy_id int NOT NULL,
    drug_id int NOT NULL,
    expiration_date datetime NOT NULL,
    FOREIGN KEY (drug_id) REFERENCES Drug(drug_id),
    FOREIGN KEY (pharmacy_id) REFERENCES Pharmacy(UID), 
    PRIMARY KEY (serial_number, pharmacy_id, drug_id)
);

CREATE TABLE IF NOT EXISTS Order_Contains_Drug(
    order_id int,
    drug_id int,
    prescription_id int NOT NULL,
    count int NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Drug_Order(order_id),
    FOREIGN KEY (drug_id) REFERENCES Drug(drug_id),
    FOREIGN KEY (prescription_id) REFERENCES Prescription(prescription_id),
    PRIMARY KEY (order_id, drug_id),
    CHECK (count > 0)
);

CREATE TRIGGER doctor_inserted
AFTER INSERT ON Doctor FOR EACH ROW
	INSERT INTO Role (UID, role) VALUES (new.UID, "Doctor");

CREATE TRIGGER pharmacy_inserted
AFTER INSERT ON Pharmacy FOR EACH ROW
	INSERT INTO Role (UID, role) VALUES (new.UID, "Pharmacy");

CREATE TRIGGER patient_inserted
AFTER INSERT ON Patient FOR EACH ROW
	INSERT INTO Role (UID, role) VALUES (new.UID, "Patient");