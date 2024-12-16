-- Create the database
CREATE DATABASE HealthcareSystem;
USE HealthcareSystem;

-- Create the Users table (Super-Entity)
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role ENUM('Patient', 'Doctor', 'Admin') NOT NULL,
    profile_picture VARCHAR(255),
    gender ENUM('Male', 'Female'),
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Patients table (Sub-Entity)
CREATE TABLE Patients (
    patient_id INT PRIMARY KEY,
    FOREIGN KEY (patient_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    height FLOAT,
    weight FLOAT,
    blood_type VARCHAR(3),
    chronic_conditions TEXT,
    emergency_contact VARCHAR(255)
);

-- Create the Doctors table (Sub-Entity)
CREATE TABLE Doctors (
    doctor_id INT PRIMARY KEY,
    FOREIGN KEY (doctor_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    specialization VARCHAR(255),
    license_number VARCHAR(50) UNIQUE,
    hospital_affiliation VARCHAR(255)
);

-- Create the Admins table (Sub-Entity)
CREATE TABLE Admins (
    admin_id INT PRIMARY KEY,
    FOREIGN KEY (admin_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    privileges TEXT,
    last_login TIMESTAMP
);

-- Create the Health Metrics table
CREATE TABLE Health_Metrics (
    metric_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    heart_rate INT,
    blood_pressure VARCHAR(20),
    activity_level INT,
    sleep_quality INT,
    wellness INT,
    date_time DATETIME NOT NULL
);

-- Create the Appointments table
CREATE TABLE Appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    doctor_id INT,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id) ON DELETE CASCADE,
    date_time DATETIME NOT NULL,
    status ENUM('Pending', 'Confirmed', 'Cancelled') NOT NULL,
    reason TEXT
);

-- Create the Medications table
CREATE TABLE Medications (
    medication_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    doctor_id INT,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id) ON DELETE CASCADE,
    medication_name VARCHAR(255) NOT NULL,
    dosage VARCHAR(50),
    start_date DATE NOT NULL,
    end_date DATE,
    instructions TEXT
);

-- Create the Medical Reports table
CREATE TABLE Medical_Reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    doctor_id INT,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id) ON DELETE CASCADE,
    report_date DATE NOT NULL,
    diagnosis TEXT NOT NULL,
    recommendations TEXT
);

-- Create the Chats table
CREATE TABLE Chats (
    chat_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    FOREIGN KEY (sender_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    receiver_id INT,
    FOREIGN KEY (receiver_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    timestamp DATETIME NOT NULL
);

-- Create the Emergency Actions table
CREATE TABLE Emergency_Actions (
    emergency_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    action_date DATETIME NOT NULL,
    action_type VARCHAR(255) NOT NULL,
    remarks TEXT
);

-- Insert roles as an ENUM in the Users table for role differentiation
-- First, insert users for 100 patients
INSERT INTO Users (user_id, name, email, password, phone, role, profile_picture, gender, age)
VALUES
(101, 'Dr. Ahmed Saleh', 'ahmed.saleh@example.com', 'password123', '01012345678', 'Doctor', NULL, 'Male', 45),
(102, 'Dr. Mona Ali', 'mona.ali@example.com', 'password123', '01023456789', 'Doctor', NULL, 'Female', 38),
(103, 'Dr. Youssef Khaled', 'youssef.khaled@example.com', 'password123', '01034567890', 'Doctor', NULL, 'Male', 50),
(104, 'Dr. Samar Hossam', 'samar.hossam@example.com', 'password123', '01045678901', 'Doctor', NULL, 'Female', 42);


-- Now, integrate these users with the patients table using user_id
INSERT INTO Patients (patient_id, height, weight, blood_type, chronic_conditions, emergency_contact) VALUES
(1, 170, 75, 'O+', 'None', '01234567890'),
(2, 160, 60, 'A+', 'Diabetes', '01234567891'),
(3, 165, 70, 'B+', 'Asthma', '01234567892'),
(4, 180, 80, 'AB+', 'None', '01234567893'),
(5, 175, 85, 'O-', 'Hypertension', '01234567894'),
(6, 155, 65, 'A-', 'None', '01234567895'),
(7, 162, 68, 'B-', 'None', '01234567896'),
(8, 169, 73, 'AB-', 'None', '01234567897'),
(9, 174, 78, 'O+', 'Cholesterol', '01234567898'),
(10, 168, 72, 'A+', 'None', '01234567899'),
(11, 166, 71, 'B+', 'Asthma', '01234567900'),
(12, 160, 63, 'AB+', 'None', '01234567901'),
(13, 172, 77, 'O-', 'None', '01234567902'),
(14, 180, 80, 'A+', 'Hypertension', '01234567903'),
(15, 167, 69, 'B-', 'None', '01234567904'),
(16, 178, 74, 'O+', 'Diabetes', '01234567905'),
(17, 165, 66, 'AB-', 'None', '01234567906'),
(18, 170, 70, 'A+', 'Cholesterol', '01234567907'),
(19, 162, 64, 'B+', 'Asthma', '01234567908'),
(20, 175, 82, 'O-', 'None', '01234567909');


-- Insert Health Metrics for the first 20 patients
INSERT INTO Health_Metrics (metric_id, heart_rate, blood_pressure, activity_level, sleep_quality, wellness, date_time, patient_id) VALUES
(1, 75, '120/80', 'Moderate', 7, 'Good', '2024-12-01 08:30:00', 1),
(2, 82, '130/85', 'Low', 6, 'Average', '2024-12-01 09:00:00', 2),
(3, 65, '118/76', 'High', 8, 'Excellent', '2024-12-01 07:45:00', 3),
(4, 90, '140/90', 'Low', 5, 'Poor', '2024-12-01 10:15:00', 4),
(5, 72, '125/80', 'Moderate', 7, 'Good', '2024-12-01 08:00:00', 5),
(6, 88, '135/88', 'Low', 6, 'Average', '2024-12-01 09:30:00', 6),
(7, 78, '122/79', 'Moderate', 7, 'Good', '2024-12-01 08:45:00', 7),
(8, 70, '119/77', 'High', 8, 'Excellent', '2024-12-01 08:15:00', 8),
(9, 85, '138/86', 'Low', 5, 'Average', '2024-12-01 09:45:00', 9),
(10, 76, '121/80', 'Moderate', 7, 'Good', '2024-12-01 07:30:00', 10),
(11, 80, '125/85', 'Moderate', 6, 'Good', '2024-12-01 09:00:00', 11),
(12, 68, '115/75', 'High', 8, 'Excellent', '2024-12-01 07:00:00', 12),
(13, 95, '142/92', 'Low', 5, 'Poor', '2024-12-01 10:30:00', 13),
(14, 74, '124/82', 'Moderate', 7, 'Good', '2024-12-01 08:15:00', 14),
(15, 87, '137/89', 'Low', 6, 'Average', '2024-12-01 09:15:00', 15),
(16, 73, '123/78', 'Moderate', 7, 'Good', '2024-12-01 08:30:00', 16),
(17, 69, '117/76', 'High', 8, 'Excellent', '2024-12-01 07:45:00', 17),
(18, 91, '141/91', 'Low', 5, 'Poor', '2024-12-01 10:00:00', 18),
(19, 77, '120/80', 'Moderate', 7, 'Good', '2024-12-01 08:00:00', 19),
(20, 84, '130/87', 'Low', 6, 'Average', '2024-12-01 09:00:00', 20);

-- Insert medications for the 20 patients
INSERT INTO Medications (medication_id, medication_name, dosage, start_date, end_date, instructions, patient_id,doctor_id) VALUES
(1, 'Paracetamol', '500mg', '2024-01-01', '2024-01-07', 'Take one tablet every 6 hours after meals', 1,101),
(2, 'Amoxicillin', '250mg', '2024-02-01', '2024-02-10', 'Take one capsule every 8 hours with water', 2,101),
(3, 'Ibuprofen', '400mg', '2024-03-01', '2024-03-05', 'Take one tablet every 8 hours after meals', 3,101),
(4, 'Metformin', '500mg', '2024-04-01', '2024-04-30', 'Take one tablet twice a day before meals', 4,101),
(5, 'Atorvastatin', '20mg', '2024-05-01', '2024-05-30', 'Take one tablet at bedtime', 5,101),
(6, 'Salbutamol', '2 puffs', '2024-06-01', '2024-06-15', 'Use inhaler as needed for shortness of breath', 6,102),
(7, 'Losartan', '50mg', '2024-07-01', '2024-07-30', 'Take one tablet in the morning with water', 7,102),
(8, 'Cetrizine', '10mg', '2024-08-01', '2024-08-10', 'Take one tablet once a day for allergies', 8,102),
(9, 'Ranitidine', '150mg', '2024-09-01', '2024-09-10', 'Take one tablet before bedtime for acid reflux', 9,102),
(10, 'Vitamin D', '2000 IU', '2024-10-01', '2024-10-31', 'Take one capsule daily with food', 10,102),
(11, 'Omeprazole', '20mg', '2024-11-01', '2024-11-15', 'Take one tablet before breakfast', 11,103),
(12, 'Prednisolone', '5mg', '2024-12-01', '2024-12-07', 'Take one tablet three times a day after meals', 12,103),
(13, 'Hydrochlorothiazide', '25mg', '2024-01-01', '2024-01-31', 'Take one tablet in the morning with water', 13,103),
(14, 'Aspirin', '75mg', '2024-02-01', '2024-02-28', 'Take one tablet daily after breakfast', 14,103),
(15, 'Levothyroxine', '50mcg', '2024-03-01', '2024-03-31', 'Take one tablet in the morning on an empty stomach', 15,103),
(16, 'Clarithromycin', '500mg', '2024-04-01', '2024-04-14', 'Take one tablet every 12 hours with food', 16,104),
(17, 'Furosemide', '40mg', '2024-05-01', '2024-05-15', 'Take one tablet in the morning with water', 17,104),
(18, 'Insulin', '10 units', '2024-06-01', '2024-06-30', 'Inject subcutaneously before meals', 18,104),
(19, 'Montelukast', '10mg', '2024-07-01', '2024-07-31', 'Take one tablet daily in the evening', 19,104),
(20, 'Azithromycin', '500mg', '2024-08-01', '2024-08-05', 'Take one tablet once a day for five days', 20,104);

INSERT INTO Appointments (appointment_id, date_time, status, reason, patient_id, doctor_id)
VALUES
(1, '2024-12-02 09:00:00', 'Pending', 'Routine Checkup', 1, 101),
(2, '2024-12-02 11:30:00', 'Confirmed', 'Follow-up for Diabetes', 2, 101),
(3, '2024-12-03 14:00:00', 'Pending', 'Consultation for Asthma', 3, 101),
(4, '2024-12-03 16:00:00', 'Cancelled', 'General Checkup', 4, 101),
(5, '2024-12-04 10:30:00', 'Pending', 'Hypertension Follow-up', 5, 101),
(6, '2024-12-04 13:00:00', 'Pending', 'Routine Blood Work', 6, 102),
(7, '2024-12-05 08:30:00', 'Confirmed', 'Consultation for Diet', 7, 102),
(8, '2024-12-05 15:00:00', 'Pending', 'Follow-up on Cholesterol', 8, 102),
(9, '2024-12-06 09:30:00', 'Confirmed', 'Routine Checkup', 9, 102),
(10, '2024-12-06 12:00:00', 'Pending', 'Consultation for Fatigue', 10, 102),
(11, '2024-12-07 11:00:00', 'Confirmed', 'Routine Checkup', 11, 103),
(12, '2024-12-07 14:30:00', 'Pending', 'General Wellness Consultation', 12, 103),
(13, '2024-12-08 09:00:00', 'Cancelled', 'Follow-up for Asthma', 13, 103),
(14, '2024-12-08 16:00:00', 'Pending', 'Consultation for Hypertension', 14, 103),
(15, '2024-12-09 10:00:00', 'Confirmed', 'Routine Checkup', 15, 103),
(16, '2024-12-09 13:30:00', 'Pending', 'Follow-up for Cholesterol', 16, 104),
(17, '2024-12-10 08:00:00', 'Confirmed', 'Consultation for Sleep Issues', 17, 104),
(18, '2024-12-10 15:00:00', 'Pending', 'Diet and Nutrition Advice', 18, 104),
(19, '2024-12-11 11:30:00', 'Cancelled', 'Consultation for Anxiety', 19, 104),
(20, '2024-12-11 14:00:00', 'Pending', 'Follow-up for Hypertension', 20, 104);

INSERT INTO Medical_Reports (report_id, patient_id, doctor_id, report_date, diagnosis, recommendations)
VALUES
(1, 1, 101, '2024-12-02', 'Normal health, no major issues detected.', 'Continue routine health monitoring, maintain diet plan.'),
(2, 2, 101, '2024-12-02', 'Diagnosed with Diabetes, blood sugar levels above normal.', 'Adhere to medication, avoid sugar, monitor blood sugar daily.'),
(3, 3, 101, '2024-12-03', 'Mild Asthma, increased breathlessness in cold weather.', 'Use inhaler as needed, avoid cold air, regular checkups.'),
(4, 4, 101, '2024-12-03', 'General fatigue, no major conditions found.', 'Rest and hydration recommended, checkup in 1 month.'),
(5, 5, 101, '2024-12-04', 'High blood pressure, borderline hypertension.', 'Follow prescribed medication, reduce salt intake, exercise regularly.'),
(6, 6, 102, '2024-12-04', 'Routine blood work shows no significant issues.', 'Maintain a balanced diet and regular physical activity.'),
(7, 7, 102, '2024-12-05', 'Mild obesity, elevated cholesterol levels.', 'Adopt a low-fat diet, exercise regularly, and monitor cholesterol.'),
(8, 8, 102, '2024-12-05', 'Cholesterol slightly elevated, no cardiovascular risk currently.', 'Continue monitoring, improve diet, and increase physical activity.'),
(9, 9, 102, '2024-12-06', 'No major health issues found during routine checkup.', 'Keep maintaining a healthy lifestyle.'),
(10, 10, 102, '2024-12-06', 'Fatigue, suspected vitamin D deficiency.', 'Start vitamin D supplementation and regular exercise.'),
(11, 11, 103, '2024-12-07', 'Routine checkup, all vitals normal.', 'Continue healthy living, regular checkups every 6 months.'),
(12, 12, 103, '2024-12-07', 'General wellness checkup, no serious concerns found.', 'Maintain current diet, stay active, routine checkup in 6 months.'),
(13, 13, 103, '2024-12-08', 'Asthma follow-up, no significant changes since last checkup.', 'Continue medication, monitor symptoms during cold weather.'),
(14, 14, 103, '2024-12-08', 'Hypertension, blood pressure remains high.', 'Continue medication, regular blood pressure monitoring, stress management.'),
(15, 15, 103, '2024-12-09', 'Routine checkup, no issues found.', 'Maintain lifestyle, stay active, next checkup in 1 year.'),
(16, 16, 104, '2024-12-09', 'Cholesterol levels elevated, borderline hypertension.', 'Dietary changes and exercise, monitor cholesterol levels regularly.'),
(17, 17, 104, '2024-12-10', 'Sleep issues related to stress, no serious conditions detected.', 'Stress management techniques, improve sleep hygiene, follow-up in 1 month.'),
(18, 18, 104, '2024-12-10', 'Nutritional deficiencies, poor dietary habits.', 'Start nutrition supplements, improve diet with guidance from a nutritionist.'),
(19, 19, 104, '2024-12-11', 'Anxiety, stress-related health issues.', 'Start therapy, manage stress, consider anxiety medication if necessary.'),
(20, 20, 104, '2024-12-11', 'Hypertension, blood pressure elevated.', 'Continue prescribed medications, reduce sodium intake, monitor blood pressure.');

INSERT INTO Emergency_Actions (emergency_id, patient_id, action_date, action_type, remarks)
VALUES
(1, 1, '2024-12-01', 'CPR', 'Administered CPR after fainting episode'),
(2, 2, '2024-12-02', 'Hospitalization', 'Patient hospitalized for severe allergic reaction'),
(3, 3, '2024-12-03', 'Medication', 'Administered epinephrine for asthma attack'),
(4, 4, '2024-12-04', 'Ambulance', 'Patient transported to hospital after heart attack'),
(5, 5, '2024-12-05', 'CPR', 'CPR performed after sudden collapse'),
(6, 6, '2024-12-06', 'Hospitalization', 'Patient hospitalized for stroke'),
(7, 7, '2024-12-07', 'Medication', 'Administered insulin for diabetic emergency'),
(8, 8, '2024-12-08', 'CPR', 'CPR performed after cardiac arrest'),
(9, 9, '2024-12-09', 'Ambulance', 'Patient transported for a severe asthma attack'),
(10, 10, '2024-12-10', 'Hospitalization', 'Patient hospitalized after car accident'),
(11, 11, '2024-12-11', 'Medication', 'Administered pain relief for severe back injury'),
(12, 12, '2024-12-12', 'Ambulance', 'Patient transported after slipping and falling'),
(13, 13, '2024-12-13', 'CPR', 'CPR performed after drowning incident'),
(14, 14, '2024-12-14', 'Hospitalization', 'Patient hospitalized for heart complications'),
(15, 15, '2024-12-15', 'Medication', 'Administered glucose for hypoglycemic emergency'),
(16, 16, '2024-12-16', 'CPR', 'CPR administered after fainting due to low blood pressure'),
(17, 17, '2024-12-17', 'Ambulance', 'Patient transported after major injury from fall'),
(18, 18, '2024-12-18', 'Medication', 'Administered medication for acute allergic reaction'),
(19, 19, '2024-12-19', 'Hospitalization', 'Patient hospitalized for severe chest pain'),
(20, 20, '2024-12-20', 'CPR', 'CPR performed after unconsciousness due to dehydration');
-- add admins
insert into users 
values(1000,"ibrahim abd-elhady","iam.ibrahim.abd.elhadi@gmail.com","admin1235879","01141065853","Admin","","Male",20,now());