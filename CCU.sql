create database feeding_dashboard;
use feeding_dashboard;

-- Create the 'Patients' table
CREATE TABLE Patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    dob DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    admission_date DATETIME NOT NULL,
    discharge_date DATETIME NULL
);

-- Create the 'Physio_Data' Table
CREATE TABLE Physio_Data (
    data_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    measurement_time DATETIME NOT NULL,
    feed_volume FLOAT,
    oxygen_flow_rate FLOAT,
    respiratory_rate FLOAT,
    bmi FLOAT,
    fio2 FLOAT,
    peep FLOAT,
    tidal_volume FLOAT,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE
);

-- Create the 'Dietitian_Ref' Table
CREATE TABLE Dietitian_Ref (
    referral_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    referred_by VARCHAR(100) NOT NULL,
    referral_date DATETIME NOT NULL,
    status ENUM('Pending', 'Completed', 'Cancelled') DEFAULT 'Pending',
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE
);

-- Create the 'Users' Table (for Dashboard Access)
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Store hashed passwords!
    role ENUM('Admin', 'Doctor', 'Dietitian', 'Nurse') NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create the 'ML_Results' Table
CREATE TABLE ML_Results (
    ml_result_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    prediction_score FLOAT NOT NULL,
    should_refer BOOLEAN NOT NULL,
    model_used VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE
);