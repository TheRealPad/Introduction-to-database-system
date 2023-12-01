   -- Script name: inserts.sql
   -- Author:      Pierre-Alexandre Delgado-Arevalo
   -- Purpose:     insert sample data to test the integrity of this database system
   
   -- the database used to insert the data into.
   USE HealthManagementSystemDB; 
   
   -- Role table inserts
   INSERT INTO Role (name, description)
   VALUES ('admin', 'this is the super user, be kind with him'),
		  ('common', 'just common user, nothing particular'),
          ('shaman', 'A sorcerer');

-- HealthData table inserts
   INSERT INTO HealthData (height, weight, blood_pressure, breathing_rate, current_heart_rate)
   VALUE (185, 70, 10, 100, 80),
		 (285, 100, 10, 100, 60),
         (155, 10, 10, 100, 150);
   
   -- User table inserts, I use only the first 3 user, the other ones are here only to populate the roles
   INSERT INTO User (name, email, password, date_of_birth, health_metric_data_id, role_id)
   VALUES ('Pierre-Alexandre', 'pdelgadoarevalo@sfsu.edu', 'hehe', '2002-2-14', 1, 1),
		  ('Pierre', 'pierre@sfsu.edu', 'hehe', '2002-2-14', 2, 2),
		  ('Alexandre', 'alexandre@sfsu.edu', 'hehe', '2002-2-14', 3, 3),
          ('patient1', 'patient1@sfsu.edu', 'hehe', '2002-2-14', null, null),
          ('patient2', 'patient2@sfsu.edu', 'hehe', '2002-2-14', null, null),
          ('doctor1', 'doctor1@sfsu.edu', 'hehe', '2002-2-14', null, null),
          ('doctor2', 'doctor2@sfsu.edu', 'hehe', '2002-2-14', null, null),
          ('admin1', 'admin1@sfsu.edu', 'hehe', '2002-2-14', null, null),
          ('admin2', 'admin2@sfsu.edu', 'hehe', '2002-2-14', null, null);

   -- Action table inserts
   INSERT INTO Action (title, description) VALUES ('Heal', 'It heal someone'), ('Update all Health data', 'Can update any health data'), ('Driver', 'Can drive ambulance');
   
   -- Region table inserts
   INSERT INTO Region (code_area, name) VALUES ('CA', 'California'), ('NY', 'New York'), ('PA', 'Paris');
   
   -- Event table inserts
   INSERT INTO Event (title, description, place, date)
   VALUES ('Trail SF', 'Come run with me', 'San Francisco', '2010-12-31 01:15:00'),
		  ('Trail NY', 'Come run with me', 'New York', '2010-12-31 01:15:00'),
          ('Trail PA', 'Come run with me', 'Paris', '2010-12-31 01:15:00');
   
   -- Device table inserts
   INSERT INTO Device (name, description)
   VALUE ('Apple Watch', 'The watch by Apple'),
		 ('Google Pixel Watch', 'The watch by Google'),
         ('Samsung Watch', 'The watch by Samsung');
   
   -- Trainings table inserts
   INSERT INTO Training (duration, title, description)
   VALUE (10, 'Run on flat track', 'just run and enjoye'),
		 (10, 'Run on steep track', 'just run and cry'),
         (10, 'Swim', 'Enjoy the water');

   -- HealthActivity table inserts
   INSERT INTO HealthActivity (duration, title, description)
   VALUE (10, 'Yoga 1', 'Take a deep breath'),
		 (10, 'Yoga 2', 'Take a deep breath, but on one feet this time'),
		 (10, 'Tai chi', 'So different');
   
   -- FoodCategory table inserts
   INSERT INTO FoodCategory (title, description)
   VALUE ('Fast food', 'It was, however, a good intention...'),
		 ('Vegetable', 'You must eat that but you don\'t want.'),
         ('Pasta', 'Viva Italia');
   
   -- FoodExpert table inserts
   INSERT INTO FoodExpert (name, email, region)
   VALUE ('Homer J. Simpson', 'simpson@gmail.com', 'Springfield'),
		 ('Lenny', 'lenny@mail.com', 'San Francisco'),
         ('Carl', 'carl@mail.com', 'New York');

   -- Coach table inserts
   INSERT INTO Coach (name, email, sport, region)
   VALUE ('Tom Brady', 'goat@gmail.com', 'football', 'Massachussets'),
		 ('Micheal Jordan', 'wow@gmail.com', 'Basket', 'Michigan'),
         ('Messi', 'messi@gmail.com', 'soccer', 'Miami');
   
   -- Place table inserts
   INSERT INTO Place (name, position, region)
   VALUE ('San Francisco', '37° 46\' 26.2992\'\' N', 'California'),
		 ('Paris', '37° 46\' 26.2992\'\' N', 'France'),
         ('New York', '37° 46\' 26.2992\'\' N', 'New York');

   -- Language table inserts
   INSERT INTO Language (code, name) VALUE ('FR', 'French'), ('EN', 'English'), ('ES', 'Spanish');
   
   -- OS table inserts
   INSERT INTO OS (code, name) VALUE ('LINUX', 'linux'), ('MAC', 'macOS'), ('WINDOWS', 'windows');
   
   -- LicenceNum table inserts
   INSERT INTO LicenceNum (value, creation_date) VALUE ('1', '2023-11-02'), ('2', '2023-11-02'), ('3', '2023-11-02');
   
   -- Account table inserts
   INSERT INTO Account (user_id, role, region, os, language, user_health_data)
   VALUE (1, 1, 1, 1, 1, 1),
		 (2, 2, 2, 2, 2, 2),
         (3, 3, 3, 3, 3, 3);

   -- HeartRate table inserts
   INSERT INTO HeartRate (heart_rate, date, health_metric)
   VALUE (80, '2010-12-31 01:15:00', 1), (81, '2010-12-31 01:15:01', 1), (82, '2010-12-31 01:15:02', 1);
   
   -- ActionLinkToRole table inserts
   INSERT INTO ActionLinkToRole (action, role) VALUE (1, 1), (1, 2), (1, 3);
   
   -- AccountHasAction table inserts
   INSERT INTO AccountHasAction (action, account) VALUE (1, 1), (1, 2), (1, 3);
   
   -- AccountSavePlace table inserts
   INSERT INTO AccountSavePlace (account, place) VALUE (1, 1), (2, 2), (3, 3);
   
   -- AccountSaveCoach table inserts
   INSERT INTO AccountSaveCoach (account, coach) VALUE (1, 1), (2, 2), (3, 3);
   
   -- AccountSaveFoodExpert table inserts
   INSERT INTO AccountSaveFoodExpert (account, food_expert) VALUE (1, 1), (2, 2), (3, 3);
   
   -- AccountSaveFoodCategory table inserts
   INSERT INTO AccountSaveFoodCategory (account, food_category) VALUE (1, 1), (2, 2), (3, 3);
   
   -- AccountSaveHealthActivity table inserts
   INSERT INTO AccountSaveHealthActivity (account, health_activity) VALUE (1, 1), (2, 2), (3, 3);
   
   -- AccountSaveTraining table inserts
   INSERT INTO AccountSaveTraining (account, training) VALUE (1, 1), (2, 2), (3, 3);
   
   -- AccountAssociateToDevice table inserts
   INSERT INTO AccountAssociateToDevice (account, device) VALUE (1, 1), (2, 2), (3, 3);
   
   -- AccountRegisterToEvent table inserts
   INSERT INTO AccountRegisterToEvent (account, event) VALUE (1, 1), (2, 2), (3, 3);
          
-- UserLinkToUser table inserts
   INSERT INTO UserLinkToUser (userA, userB) VALUES (1, 2), (1, 3), (3, 2);
   
-- SocialNumber table inserts
   INSERT INTO SocialNumber (value, user) VALUE ('1', 1), ('2', 2), ('3', 3);
   
-- Meal table inserts
   INSERT INTO Meal (title, description, caloric_value, date, user)
   VALUE ('Birthday', 'A big cake with lots of sugar', 100, '2023-2-14', 1),
		 ('monday lunch', 'Some vegetables', 10, '2023-2-14', 2),
         ('Party', 'Pizza pizza and more pizza', 100, '2023-2-14', 1);
         
-- SportActivity table inserts
   INSERT INTO SportActivity (title, description, duration, user)
   VALUE ("run 1", "run 10km", 60, 1),
		 ("run 2", "run 8km", 60, 1),
         ("run 3", "run 12km", 60, 1);
         
-- Admin table inserts
INSERT INTO Admin (user, name) VALUES (1, 'first admin'), (2, 'second admin'), (3, 'last admin');

-- User table inserts
INSERT INTO Patient (user, name) VALUES (1, 'first patient'), (2, 'second patient'), (3, 'last patient');

-- Doctor table inserts
INSERT INTO Doctor (licence, speciality, user) VALUES (1, 'Skin', 1), (2, 'Mucle', 2), (3, 'General', 3);
