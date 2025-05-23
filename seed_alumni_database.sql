-- sample passwords: password123
-- Insert sample users
INSERT INTO users (email, password_hash, is_active, is_admin, created_at, email_verified)
VALUES 
('admin@example.com', 'scrypt:32768:8:1$g9RJOV74cFO2vsbi$644d8891dfd1af34f53cf3273dd9e9329cd52f49dd6b81b912ba910efed29552dd5ce48db073b0f801288f5dada75eca889311ecaac026d87f48ed86a71d1d34', TRUE, TRUE, CURRENT_TIMESTAMP, TRUE),
('john.doe@example.com', 'scrypt:32768:8:1$g9RJOV74cFO2vsbi$644d8891dfd1af34f53cf3273dd9e9329cd52f49dd6b81b912ba910efed29552dd5ce48db073b0f801288f5dada75eca889311ecaac026d87f48ed86a71d1d34', TRUE, FALSE, CURRENT_TIMESTAMP, TRUE),
('jane.smith@example.com', 'scrypt:32768:8:1$g9RJOV74cFO2vsbi$644d8891dfd1af34f53cf3273dd9e9329cd52f49dd6b81b912ba910efed29552dd5ce48db073b0f801288f5dada75eca889311ecaac026d87f48ed86a71d1d34', TRUE, FALSE, CURRENT_TIMESTAMP, TRUE),
('michael.johnson@example.com', 'scrypt:32768:8:1$g9RJOV74cFO2vsbi$644d8891dfd1af34f53cf3273dd9e9329cd52f49dd6b81b912ba910efed29552dd5ce48db073b0f801288f5dada75eca889311ecaac026d87f48ed86a71d1d34', TRUE, FALSE, CURRENT_TIMESTAMP, TRUE),
('sarah.williams@example.com', 'scrypt:32768:8:1$g9RJOV74cFO2vsbi$644d8891dfd1af34f53cf3273dd9e9329cd52f49dd6b81b912ba910efed29552dd5ce48db073b0f801288f5dada75eca889311ecaac026d87f48ed86a71d1d34', TRUE, FALSE, CURRENT_TIMESTAMP, TRUE);

-- Insert admin
INSERT INTO admins (user_id, first_name, last_name, role)
VALUES (1, 'System', 'Admin', 'Super Admin');

-- Insert sample alumni
INSERT INTO alumni (user_id, first_name, last_name, middle_name, phone, date_of_birth, profile_photo, bio, 
                   matriculation_number, faculty, department, graduation_year, degree, 
                   job_title, organization, industry, linkedin_url, show_email, show_phone, show_job)
VALUES 
(2, 'John', 'Doe', NULL, '+2341234567890', '1990-05-15', '/static/img/profiles/john.jpg', 
 'Experienced software engineer with a passion for AI and machine learning.', 
 'FUO/2010/001', 'Science', 'Computer Science', 2014, 'BSc', 
 'Senior Software Engineer', 'Tech Innovations Inc.', 'Information Technology', 
 'https://linkedin.com/in/johndoe', TRUE, FALSE, TRUE),

(3, 'Jane', 'Smith', 'Elizabeth', '+2349876543210', '1992-08-22', '/static/img/profiles/jane.jpg', 
 'Marketing professional specializing in digital marketing strategies.', 
 'FUO/2011/042', 'Management Sciences', 'Business Administration', 2015, 'BSc', 
 'Marketing Manager', 'Global Brands Ltd.', 'Marketing', 
 'https://linkedin.com/in/janesmith', FALSE, FALSE, TRUE),

(4, 'Michael', 'Johnson', NULL, '+2348123456789', '1988-11-30', '/static/img/profiles/michael.jpg', 
 'Civil engineer with 8 years of experience in infrastructure development.', 
 'FUO/2008/105', 'Engineering', 'Civil Engineering', 2012, 'BEng', 
 'Project Manager', 'BuildRight Construction', 'Construction', 
 'https://linkedin.com/in/michaeljohnson', TRUE, TRUE, TRUE),

(5, 'Sarah', 'Williams', 'Anne', '+2347012345678', '1993-04-10', '/static/img/profiles/sarah.jpg', 
 'Healthcare professional specializing in public health education.', 
 'FUO/2012/078', 'Nursing Sciences', 'Public Health', 2016, 'BSc', 
 'Health Education Specialist', 'National Health Foundation', 'Healthcare', 
 'https://linkedin.com/in/sarahwilliams', FALSE, FALSE, TRUE);

-- Insert sample events
INSERT INTO events (title, description, date, end_date, location, is_virtual, virtual_link, image, created_by, created_at)
VALUES 
('Annual Alumni Reunion', 'Join us for the annual reunion of FUO alumni. Network with former classmates and make new connections.',
 DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), DATE_ADD(DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), INTERVAL 8 HOUR),
 'FUO Main Campus, Auditorium', FALSE, NULL, '/static/img/events/reunion.jpg', 1, CURRENT_TIMESTAMP),

('Career Development Workshop', 'Learn essential skills for career advancement in this interactive workshop led by industry experts.',
 DATE_ADD(CURRENT_DATE, INTERVAL 15 DAY), DATE_ADD(DATE_ADD(CURRENT_DATE, INTERVAL 15 DAY), INTERVAL 3 HOUR),
 NULL, TRUE, 'https://zoom.us/j/123456789', '/static/img/events/workshop.jpg', 1, CURRENT_TIMESTAMP),

('Homecoming Weekend', 'A weekend full of activities to celebrate our alma mater and reconnect with fellow alumni.',
 DATE_ADD(CURRENT_DATE, INTERVAL 60 DAY), DATE_ADD(CURRENT_DATE, INTERVAL 62 DAY),
 'FUO Campus', FALSE, NULL, '/static/img/events/homecoming.jpg', 1, CURRENT_TIMESTAMP),

('Virtual Networking Night', 'Connect with alumni from around the world in this virtual networking event.',
 DATE_ADD(CURRENT_DATE, INTERVAL 7 DAY), DATE_ADD(DATE_ADD(CURRENT_DATE, INTERVAL 7 DAY), INTERVAL 2 HOUR),
 NULL, TRUE, 'https://zoom.us/j/987654321', '/static/img/events/networking.jpg', 1, CURRENT_TIMESTAMP);


-- Insert sample projects for fundraising
INSERT INTO projects (title, description, goal_amount, current_amount, image, start_date, end_date, is_active, created_by, created_at)
VALUES 
('Library Expansion Fund', 'Help us expand the university library to accommodate more resources and study spaces for students.', 
 5000000.00, 1250000.00, '/static/img/projects/library.jpg', CURRENT_DATE - INTERVAL 30 DAY, 
 CURRENT_DATE + INTERVAL 150 DAY, TRUE, 1, CURRENT_TIMESTAMP),

('Scholarship Fund', 'Support deserving students with financial needs through our scholarship program.', 
 3000000.00, 900000.00, '/static/img/projects/scholarship.jpg', CURRENT_DATE - INTERVAL 60 DAY, 
 CURRENT_DATE + INTERVAL 120 DAY, TRUE, 1, CURRENT_TIMESTAMP),

('Innovation Lab', 'Contribute to the creation of a state-of-the-art innovation lab for students to develop practical skills.', 
 7500000.00, 2000000.00, '/static/img/projects/lab.jpg', CURRENT_DATE - INTERVAL 15 DAY, 
 CURRENT_DATE + INTERVAL 165 DAY, TRUE, 1, CURRENT_TIMESTAMP),

('Sports Complex Renovation', 'Help renovate the university sports complex to provide better facilities for student athletes.', 
 4000000.00, 500000.00, '/static/img/projects/sports.jpg', CURRENT_DATE, 
 CURRENT_DATE + INTERVAL 180 DAY, TRUE, 1, CURRENT_TIMESTAMP);

-- Insert sample contributions
INSERT INTO contributions (alumni_id, project_id, amount, payment_method, transaction_id, is_anonymous, dedication, created_at)
VALUES 
(1, 1, 50000.00, 'Credit Card', 'TXN123456789', FALSE, NULL, CURRENT_TIMESTAMP - INTERVAL 25 DAY),
(2, 1, 100000.00, 'Bank Transfer', 'TXN234567890', FALSE, 'In memory of Prof. James Wilson', CURRENT_TIMESTAMP - INTERVAL 20 DAY),
(3, 2, 75000.00, 'Credit Card', 'TXN345678901', TRUE, NULL, CURRENT_TIMESTAMP - INTERVAL 15 DAY),
(4, 3, 200000.00, 'Bank Transfer', 'TXN456789012', FALSE, NULL, CURRENT_TIMESTAMP - INTERVAL 10 DAY),
(1, 2, 25000.00, 'Credit Card', 'TXN567890123', FALSE, NULL, CURRENT_TIMESTAMP - INTERVAL 5 DAY),
(2, 3, 150000.00, 'Bank Transfer', 'TXN678901234', FALSE, 'For future innovators', CURRENT_TIMESTAMP - INTERVAL 3 DAY);


-- Insert sample event attendees
INSERT INTO event_attendees (event_id, alumni_id, status, registered_at)
VALUES 
(1, 1, 'registered', CURRENT_TIMESTAMP - INTERVAL 20 DAY),
(1, 2, 'registered', CURRENT_TIMESTAMP - INTERVAL 18 DAY),
(1, 3, 'registered', CURRENT_TIMESTAMP - INTERVAL 15 DAY),
(2, 1, 'registered', CURRENT_TIMESTAMP - INTERVAL 10 DAY),
(2, 4, 'registered', CURRENT_TIMESTAMP - INTERVAL 8 DAY),
(3, 2, 'registered', CURRENT_TIMESTAMP - INTERVAL 5 DAY),
(3, 3, 'registered', CURRENT_TIMESTAMP - INTERVAL 4 DAY),
(4, 1, 'registered', CURRENT_TIMESTAMP - INTERVAL 3 DAY),
(4, 4, 'registered', CURRENT_TIMESTAMP - INTERVAL 2 DAY);

-- Insert sample announcements
INSERT INTO announcements (title, content, is_published, created_by, created_at)
VALUES 
('Welcome to the New Alumni Portal', 'We are excited to launch our new alumni portal. Explore the features and stay connected with your alma mater.', 
 TRUE, 1, CURRENT_TIMESTAMP - INTERVAL 30 DAY),

('Upcoming Alumni Association Elections', 'The elections for the Alumni Association Executive Committee will be held next month. Nominations are now open.', 
 TRUE, 1, CURRENT_TIMESTAMP - INTERVAL 15 DAY),

('New Career Services Available', 'We have partnered with leading companies to provide exclusive career opportunities for our alumni. Check the career section for more details.', 
 TRUE, 1, CURRENT_TIMESTAMP - INTERVAL 7 DAY),

('Alumni Magazine: Call for Submissions', 'We are accepting submissions for the next issue of our alumni magazine. Share your success stories, articles, or creative works.', 
 TRUE, 1, CURRENT_TIMESTAMP - INTERVAL 3 DAY);

