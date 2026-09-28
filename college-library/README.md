# College Library Management System

A Spring Boot + MySQL complete web application for managing a college library.

## Setup Instructions for VS Code

### Step 1
Ensure you have installed:
- JDK 17
- Maven
- MySQL Server
- VS Code (with Java extensions)

### Step 2
Create the database in MySQL:
```sql
CREATE DATABASE college_library;
```

### Step 3
Update `src/main/resources/application.properties` with your MySQL username and password.
```properties
spring.datasource.username=root
spring.datasource.password=YOUR_MYSQL_PASSWORD
```

### Step 4
Open terminal in `college-library` directory and run:
```bash
mvn clean install
```

### Step 5
Run the application:
```bash
mvn spring-boot:run
```

### Step 6
Open the application in your browser:
http://localhost:8080/

### Testing via Postman
**Add Book:** `POST /api/books`
```json
{
  "title": "Java Programming",
  "author": "Herbert Schildt",
  "isbn": "9780000000001",
  "category": "Computer Science",
  "totalCopies": 5
}
```

**Add Student:** `POST /api/students`
```json
{
  "studentId": "CSE001",
  "name": "Student One",
  "department": "CSE",
  "year": 3,
  "email": "student@example.com",
  "phone": "9876543210"
}
```

**Issue Book:** `POST /api/issues`
```json
{
  "studentId": 1,
  "bookId": 1
}
```
