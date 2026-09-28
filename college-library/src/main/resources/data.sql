INSERT IGNORE INTO books (title, author, isbn, category, total_copies, available_copies, created_at, updated_at) VALUES 
('Java Programming', 'Herbert Schildt', '9780000000001', 'Computer Science', 5, 5, NOW(), NOW()),
('Database Management Systems', 'Raghu Ramakrishnan', '9780000000002', 'Computer Science', 3, 3, NOW(), NOW()),
('Operating Systems', 'Silberschatz', '9780000000003', 'Computer Science', 4, 4, NOW(), NOW()),
('Computer Networks', 'Andrew S. Tanenbaum', '9780000000004', 'Computer Science', 6, 6, NOW(), NOW()),
('Software Engineering', 'Ian Sommerville', '9780000000005', 'Computer Science', 2, 2, NOW(), NOW());

INSERT IGNORE INTO students (student_id, name, department, year, email, phone) VALUES 
('CSE001', 'Alice Smith', 'CSE', 3, 'alice@example.com', '9876543210'),
('CSE002', 'Bob Johnson', 'CSE', 2, 'bob@example.com', '9876543211'),
('ECE001', 'Charlie Brown', 'ECE', 4, 'charlie@example.com', '9876543212'),
('MEC001', 'David Lee', 'MEC', 1, 'david@example.com', '9876543213'),
('CIV001', 'Eve Davis', 'CIV', 3, 'eve@example.com', '9876543214');
