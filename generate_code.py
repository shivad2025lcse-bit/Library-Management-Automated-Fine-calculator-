import os
import zipfile
import urllib.request

base_dir = r"d:\LibraryManagement.java"
os.chdir(base_dir)

# Download Spring Boot project
url = "https://start.spring.io/starter.zip?dependencies=web,data-jpa,validation,mysql&type=maven-project&language=java&javaVersion=17&groupId=com.college&artifactId=library&name=college-library&packageName=com.college.library"
urllib.request.urlretrieve(url, "library.zip")

with zipfile.ZipFile("library.zip", 'r') as zip_ref:
    zip_ref.extractall("college-library")

os.remove("library.zip")

code_files = {
    "college-library/src/main/resources/application.properties": """spring.application.name=college-library

spring.datasource.url=jdbc:mysql://localhost:3306/college_library
spring.datasource.username=root
spring.datasource.password=YOUR_MYSQL_PASSWORD

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.format_sql=true

server.port=8080
""",
    "college-library/src/main/java/com/college/library/entity/IssueStatus.java": """package com.college.library.entity;

public enum IssueStatus {
    ISSUED,
    RETURNED
}
""",
    "college-library/src/main/java/com/college/library/entity/Book.java": """package com.college.library.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import java.time.LocalDateTime;

@Entity
@Table(name = "books")
public class Book {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Title is required")
    private String title;

    @NotBlank(message = "Author is required")
    private String author;

    @Column(unique = true, nullable = false)
    @NotBlank(message = "ISBN is required")
    private String isbn;

    @NotBlank(message = "Category is required")
    private String category;

    @NotNull
    @Positive(message = "Total copies must be greater than zero")
    private Integer totalCopies;

    @NotNull
    private Integer availableCopies;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author; }
    public String getIsbn() { return isbn; }
    public void setIsbn(String isbn) { this.isbn = isbn; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public Integer getTotalCopies() { return totalCopies; }
    public void setTotalCopies(Integer totalCopies) { this.totalCopies = totalCopies; }
    public Integer getAvailableCopies() { return availableCopies; }
    public void setAvailableCopies(Integer availableCopies) { this.availableCopies = availableCopies; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}
""",
    "college-library/src/main/java/com/college/library/entity/Student.java": """package com.college.library.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.util.List;

@Entity
@Table(name = "students")
public class Student {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    @Column(unique = true, nullable = false)
    private String studentId;

    @NotBlank
    private String name;

    @NotBlank
    private String department;

    @NotNull
    private Integer year;

    @Email
    @NotBlank
    private String email;

    @NotBlank
    private String phone;

    @OneToMany(mappedBy = "student")
    private List<BookIssue> bookIssues;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getStudentId() { return studentId; }
    public void setStudentId(String studentId) { this.studentId = studentId; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDepartment() { return department; }
    public void setDepartment(String department) { this.department = department; }
    public Integer getYear() { return year; }
    public void setYear(Integer year) { this.year = year; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }
    public List<BookIssue> getBookIssues() { return bookIssues; }
    public void setBookIssues(List<BookIssue> bookIssues) { this.bookIssues = bookIssues; }
}
""",
    "college-library/src/main/java/com/college/library/entity/BookIssue.java": """package com.college.library.entity;

import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
@Table(name = "book_issues")
public class BookIssue {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "student_id", nullable = false)
    private Student student;

    @ManyToOne
    @JoinColumn(name = "book_id", nullable = false)
    private Book book;

    @Column(nullable = false)
    private LocalDate issueDate;

    @Column(nullable = false)
    private LocalDate dueDate;

    private LocalDate returnDate;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private IssueStatus status;

    private Integer fineAmount = 0;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Student getStudent() { return student; }
    public void setStudent(Student student) { this.student = student; }
    public Book getBook() { return book; }
    public void setBook(Book book) { this.book = book; }
    public LocalDate getIssueDate() { return issueDate; }
    public void setIssueDate(LocalDate issueDate) { this.issueDate = issueDate; }
    public LocalDate getDueDate() { return dueDate; }
    public void setDueDate(LocalDate dueDate) { this.dueDate = dueDate; }
    public LocalDate getReturnDate() { return returnDate; }
    public void setReturnDate(LocalDate returnDate) { this.returnDate = returnDate; }
    public IssueStatus getStatus() { return status; }
    public void setStatus(IssueStatus status) { this.status = status; }
    public Integer getFineAmount() { return fineAmount; }
    public void setFineAmount(Integer fineAmount) { this.fineAmount = fineAmount; }
}
""",
    "college-library/src/main/java/com/college/library/repository/BookRepository.java": """package com.college.library.repository;

import com.college.library.entity.Book;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface BookRepository extends JpaRepository<Book, Long> {
    List<Book> findByCategory(String category);
    
    @Query("SELECT b FROM Book b WHERE LOWER(b.title) LIKE LOWER(CONCAT('%', :keyword, '%')) OR LOWER(b.author) LIKE LOWER(CONCAT('%', :keyword, '%')) OR LOWER(b.category) LIKE LOWER(CONCAT('%', :keyword, '%'))")
    List<Book> searchBooks(@Param("keyword") String keyword);
    
    List<Book> findByTitleContainingIgnoreCaseOrAuthorContainingIgnoreCaseOrCategoryContainingIgnoreCase(String title, String author, String category);
}
""",
    "college-library/src/main/java/com/college/library/repository/StudentRepository.java": """package com.college.library.repository;

import com.college.library.entity.Student;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StudentRepository extends JpaRepository<Student, Long> {
}
""",
    "college-library/src/main/java/com/college/library/repository/BookIssueRepository.java": """package com.college.library.repository;

import com.college.library.entity.BookIssue;
import com.college.library.entity.IssueStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.time.LocalDate;
import java.util.List;

public interface BookIssueRepository extends JpaRepository<BookIssue, Long> {
    List<BookIssue> findByStudentIdAndStatus(Long studentId, IssueStatus status);
    List<BookIssue> findByStudentId(Long studentId);
    List<BookIssue> findByStatus(IssueStatus status);
    boolean existsByBookIdAndStatus(Long bookId, IssueStatus status);
    
    @Query("SELECT SUM(bi.fineAmount) FROM BookIssue bi")
    Integer getTotalFine();
}
""",
    "college-library/src/main/java/com/college/library/exception/ResourceNotFoundException.java": """package com.college.library.exception;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}
""",
    "college-library/src/main/java/com/college/library/exception/BadRequestException.java": """package com.college.library.exception;

public class BadRequestException extends RuntimeException {
    public BadRequestException(String message) {
        super(message);
    }
}
""",
    "college-library/src/main/java/com/college/library/exception/GlobalExceptionHandler.java": """package com.college.library.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<Map<String, String>> handleResourceNotFound(ResourceNotFoundException ex) {
        Map<String, String> response = new HashMap<>();
        response.put("error", ex.getMessage());
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(BadRequestException.class)
    public ResponseEntity<Map<String, String>> handleBadRequest(BadRequestException ex) {
        Map<String, String> response = new HashMap<>();
        response.put("error", ex.getMessage());
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, String>> handleValidationExceptions(MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getAllErrors().forEach((error) -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
        });
        return new ResponseEntity<>(errors, HttpStatus.BAD_REQUEST);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, String>> handleGenericException(Exception ex) {
        Map<String, String> response = new HashMap<>();
        response.put("error", ex.getMessage());
        return new ResponseEntity<>(response, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
""",
    "college-library/src/main/java/com/college/library/service/BookService.java": """package com.college.library.service;

import com.college.library.entity.Book;
import com.college.library.entity.IssueStatus;
import com.college.library.exception.BadRequestException;
import com.college.library.exception.ResourceNotFoundException;
import com.college.library.repository.BookIssueRepository;
import com.college.library.repository.BookRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class BookService {
    @Autowired
    private BookRepository bookRepository;
    
    @Autowired
    private BookIssueRepository bookIssueRepository;

    public Book addBook(Book book) {
        book.setAvailableCopies(book.getTotalCopies());
        return bookRepository.save(book);
    }

    public List<Book> getAllBooks() {
        return bookRepository.findAll();
    }

    public Book getBookById(Long id) {
        return bookRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + id));
    }

    public Book updateBook(Long id, Book bookDetails) {
        Book book = getBookById(id);
        book.setTitle(bookDetails.getTitle());
        book.setAuthor(bookDetails.getAuthor());
        book.setIsbn(bookDetails.getIsbn());
        book.setCategory(bookDetails.getCategory());
        
        int issued = book.getTotalCopies() - book.getAvailableCopies();
        if(bookDetails.getTotalCopies() < issued) {
            throw new BadRequestException("Total copies cannot be less than currently issued copies");
        }
        
        book.setTotalCopies(bookDetails.getTotalCopies());
        book.setAvailableCopies(bookDetails.getTotalCopies() - issued);
        
        return bookRepository.save(book);
    }

    public void deleteBook(Long id) {
        Book book = getBookById(id);
        if(bookIssueRepository.existsByBookIdAndStatus(id, IssueStatus.ISSUED)) {
            throw new BadRequestException("Cannot delete book. Copies are currently issued.");
        }
        bookRepository.delete(book);
    }

    public List<Book> searchBooks(String keyword, String title, String author, String category) {
        if (keyword != null && !keyword.isEmpty()) {
            return bookRepository.searchBooks(keyword);
        }
        if (title != null || author != null || category != null) {
            return bookRepository.findByTitleContainingIgnoreCaseOrAuthorContainingIgnoreCaseOrCategoryContainingIgnoreCase(
                title != null ? title : "", 
                author != null ? author : "", 
                category != null ? category : ""
            );
        }
        return bookRepository.findAll();
    }
}
""",
    "college-library/src/main/java/com/college/library/service/StudentService.java": """package com.college.library.service;

import com.college.library.entity.Student;
import com.college.library.exception.ResourceNotFoundException;
import com.college.library.repository.StudentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class StudentService {
    @Autowired
    private StudentRepository studentRepository;

    public Student addStudent(Student student) {
        return studentRepository.save(student);
    }

    public List<Student> getAllStudents() {
        return studentRepository.findAll();
    }

    public Student getStudentById(Long id) {
        return studentRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Student not found with id: " + id));
    }

    public Student updateStudent(Long id, Student studentDetails) {
        Student student = getStudentById(id);
        student.setName(studentDetails.getName());
        student.setDepartment(studentDetails.getDepartment());
        student.setYear(studentDetails.getYear());
        student.setEmail(studentDetails.getEmail());
        student.setPhone(studentDetails.getPhone());
        return studentRepository.save(student);
    }

    public void deleteStudent(Long id) {
        Student student = getStudentById(id);
        studentRepository.delete(student);
    }
}
""",
    "college-library/src/main/java/com/college/library/service/BookIssueService.java": """package com.college.library.service;

import com.college.library.entity.Book;
import com.college.library.entity.BookIssue;
import com.college.library.entity.IssueStatus;
import com.college.library.entity.Student;
import com.college.library.exception.BadRequestException;
import com.college.library.exception.ResourceNotFoundException;
import com.college.library.repository.BookIssueRepository;
import com.college.library.repository.BookRepository;
import com.college.library.repository.StudentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class BookIssueService {
    @Autowired
    private BookIssueRepository bookIssueRepository;
    @Autowired
    private BookRepository bookRepository;
    @Autowired
    private StudentRepository studentRepository;

    private static final int FINE_PER_DAY = 10;
    private static final int ISSUE_DAYS = 14;

    @Transactional
    public BookIssue issueBook(Long studentId, Long bookId) {
        Student student = studentRepository.findById(studentId)
                .orElseThrow(() -> new ResourceNotFoundException("Student not found"));
        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found"));

        if (book.getAvailableCopies() <= 0) {
            throw new BadRequestException("No copies of this book are currently available.");
        }

        book.setAvailableCopies(book.getAvailableCopies() - 1);
        bookRepository.save(book);

        BookIssue issue = new BookIssue();
        issue.setStudent(student);
        issue.setBook(book);
        issue.setIssueDate(LocalDate.now());
        issue.setDueDate(LocalDate.now().plusDays(ISSUE_DAYS));
        issue.setStatus(IssueStatus.ISSUED);
        issue.setFineAmount(0);

        return bookIssueRepository.save(issue);
    }

    @Transactional
    public BookIssue returnBook(Long issueId) {
        BookIssue issue = bookIssueRepository.findById(issueId)
                .orElseThrow(() -> new ResourceNotFoundException("Issue record not found"));

        if (issue.getStatus() == IssueStatus.RETURNED) {
            throw new BadRequestException("Book already returned");
        }

        issue.setReturnDate(LocalDate.now());
        issue.setStatus(IssueStatus.RETURNED);
        issue.setFineAmount(calculateFine(issue.getDueDate(), issue.getReturnDate()));

        Book book = issue.getBook();
        book.setAvailableCopies(book.getAvailableCopies() + 1);
        bookRepository.save(book);

        return bookIssueRepository.save(issue);
    }
    
    public int calculateFine(LocalDate dueDate, LocalDate returnDate) {
        if(returnDate.isBefore(dueDate) || returnDate.isEqual(dueDate)) return 0;
        long overdueDays = ChronoUnit.DAYS.between(dueDate, returnDate);
        return (int) overdueDays * FINE_PER_DAY;
    }

    public List<BookIssue> getCurrentlyIssuedBooksByStudent(Long studentId) {
        List<BookIssue> issues = bookIssueRepository.findByStudentIdAndStatus(studentId, IssueStatus.ISSUED);
        issues.forEach(i -> i.setFineAmount(calculateFine(i.getDueDate(), LocalDate.now())));
        return issues;
    }

    public List<BookIssue> getStudentHistory(Long studentId) {
        return bookIssueRepository.findByStudentId(studentId);
    }

    public List<BookIssue> getAllIssuedBooks() {
        List<BookIssue> issues = bookIssueRepository.findByStatus(IssueStatus.ISSUED);
        issues.forEach(i -> i.setFineAmount(calculateFine(i.getDueDate(), LocalDate.now())));
        return issues;
    }
}
""",
    "college-library/src/main/java/com/college/library/controller/BookController.java": """package com.college.library.controller;

import com.college.library.entity.Book;
import com.college.library.service.BookService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/books")
@CrossOrigin("*")
public class BookController {
    @Autowired
    private BookService bookService;

    @PostMapping
    public ResponseEntity<Book> addBook(@Valid @RequestBody Book book) {
        return ResponseEntity.ok(bookService.addBook(book));
    }

    @GetMapping
    public ResponseEntity<List<Book>> getAllBooks(@RequestParam(required = false) String category) {
        if(category != null && !category.isEmpty()) {
            return ResponseEntity.ok(bookService.searchBooks(null, null, null, category));
        }
        return ResponseEntity.ok(bookService.getAllBooks());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Book> getBookById(@PathVariable Long id) {
        return ResponseEntity.ok(bookService.getBookById(id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Book> updateBook(@PathVariable Long id, @Valid @RequestBody Book book) {
        return ResponseEntity.ok(bookService.updateBook(id, book));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteBook(@PathVariable Long id) {
        bookService.deleteBook(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/search")
    public ResponseEntity<List<Book>> searchBooks(
            @RequestParam(required = false) String keyword,
            @RequestParam(required = false) String title,
            @RequestParam(required = false) String author,
            @RequestParam(required = false) String category) {
        return ResponseEntity.ok(bookService.searchBooks(keyword, title, author, category));
    }
}
""",
    "college-library/src/main/java/com/college/library/controller/StudentController.java": """package com.college.library.controller;

import com.college.library.entity.Student;
import com.college.library.service.StudentService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/students")
@CrossOrigin("*")
public class StudentController {
    @Autowired
    private StudentService studentService;

    @PostMapping
    public ResponseEntity<Student> addStudent(@Valid @RequestBody Student student) {
        return ResponseEntity.ok(studentService.addStudent(student));
    }

    @GetMapping
    public ResponseEntity<List<Student>> getAllStudents() {
        return ResponseEntity.ok(studentService.getAllStudents());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Student> getStudentById(@PathVariable Long id) {
        return ResponseEntity.ok(studentService.getStudentById(id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Student> updateStudent(@PathVariable Long id, @Valid @RequestBody Student student) {
        return ResponseEntity.ok(studentService.updateStudent(id, student));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteStudent(@PathVariable Long id) {
        studentService.deleteStudent(id);
        return ResponseEntity.noContent().build();
    }
}
""",
    "college-library/src/main/java/com/college/library/dto/IssueBookRequest.java": """package com.college.library.dto;

public class IssueBookRequest {
    private Long studentId;
    private Long bookId;

    public Long getStudentId() { return studentId; }
    public void setStudentId(Long studentId) { this.studentId = studentId; }
    public Long getBookId() { return bookId; }
    public void setBookId(Long bookId) { this.bookId = bookId; }
}
""",
    "college-library/src/main/java/com/college/library/controller/BookIssueController.java": """package com.college.library.controller;

import com.college.library.dto.IssueBookRequest;
import com.college.library.entity.BookIssue;
import com.college.library.service.BookIssueService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/issues")
@CrossOrigin("*")
public class BookIssueController {
    @Autowired
    private BookIssueService bookIssueService;

    @PostMapping
    public ResponseEntity<BookIssue> issueBook(@RequestBody IssueBookRequest request) {
        return ResponseEntity.ok(bookIssueService.issueBook(request.getStudentId(), request.getBookId()));
    }

    @PutMapping("/{id}/return")
    public ResponseEntity<BookIssue> returnBook(@PathVariable Long id) {
        return ResponseEntity.ok(bookIssueService.returnBook(id));
    }

    @GetMapping("/student/{studentId}")
    public ResponseEntity<List<BookIssue>> getCurrentlyIssuedBooks(@PathVariable Long studentId) {
        return ResponseEntity.ok(bookIssueService.getCurrentlyIssuedBooksByStudent(studentId));
    }

    @GetMapping("/student/{studentId}/history")
    public ResponseEntity<List<BookIssue>> getStudentHistory(@PathVariable Long studentId) {
        return ResponseEntity.ok(bookIssueService.getStudentHistory(studentId));
    }

    @GetMapping("/issued")
    public ResponseEntity<List<BookIssue>> getAllIssuedBooks() {
        return ResponseEntity.ok(bookIssueService.getAllIssuedBooks());
    }
}
""",
    "college-library/src/main/java/com/college/library/dto/DashboardResponse.java": """package com.college.library.dto;

public class DashboardResponse {
    private long totalBookRecords;
    private long totalBookCopies;
    private long availableCopies;
    private long issuedCopies;
    private long totalStudents;
    private long currentlyIssuedBooks;
    private long returnedBooks;
    private long overdueBooks;
    private long totalFine;

    // Getters and Setters
    public long getTotalBookRecords() { return totalBookRecords; }
    public void setTotalBookRecords(long totalBookRecords) { this.totalBookRecords = totalBookRecords; }
    public long getTotalBookCopies() { return totalBookCopies; }
    public void setTotalBookCopies(long totalBookCopies) { this.totalBookCopies = totalBookCopies; }
    public long getAvailableCopies() { return availableCopies; }
    public void setAvailableCopies(long availableCopies) { this.availableCopies = availableCopies; }
    public long getIssuedCopies() { return issuedCopies; }
    public void setIssuedCopies(long issuedCopies) { this.issuedCopies = issuedCopies; }
    public long getTotalStudents() { return totalStudents; }
    public void setTotalStudents(long totalStudents) { this.totalStudents = totalStudents; }
    public long getCurrentlyIssuedBooks() { return currentlyIssuedBooks; }
    public void setCurrentlyIssuedBooks(long currentlyIssuedBooks) { this.currentlyIssuedBooks = currentlyIssuedBooks; }
    public long getReturnedBooks() { return returnedBooks; }
    public void setReturnedBooks(long returnedBooks) { this.returnedBooks = returnedBooks; }
    public long getOverdueBooks() { return overdueBooks; }
    public void setOverdueBooks(long overdueBooks) { this.overdueBooks = overdueBooks; }
    public long getTotalFine() { return totalFine; }
    public void setTotalFine(long totalFine) { this.totalFine = totalFine; }
}
""",
    "college-library/src/main/java/com/college/library/controller/DashboardController.java": """package com.college.library.controller;

import com.college.library.dto.DashboardResponse;
import com.college.library.entity.Book;
import com.college.library.entity.BookIssue;
import com.college.library.entity.IssueStatus;
import com.college.library.repository.BookIssueRepository;
import com.college.library.repository.BookRepository;
import com.college.library.repository.StudentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/api/dashboard")
@CrossOrigin("*")
public class DashboardController {

    @Autowired
    private BookRepository bookRepository;
    @Autowired
    private StudentRepository studentRepository;
    @Autowired
    private BookIssueRepository bookIssueRepository;

    @GetMapping
    public ResponseEntity<DashboardResponse> getDashboardData() {
        DashboardResponse res = new DashboardResponse();
        
        List<Book> books = bookRepository.findAll();
        res.setTotalBookRecords(books.size());
        res.setTotalBookCopies(books.stream().mapToLong(Book::getTotalCopies).sum());
        res.setAvailableCopies(books.stream().mapToLong(Book::getAvailableCopies).sum());
        res.setIssuedCopies(res.getTotalBookCopies() - res.getAvailableCopies());
        
        res.setTotalStudents(studentRepository.count());
        
        List<BookIssue> issues = bookIssueRepository.findAll();
        long currentlyIssued = issues.stream().filter(i -> i.getStatus() == IssueStatus.ISSUED).count();
        long returned = issues.stream().filter(i -> i.getStatus() == IssueStatus.RETURNED).count();
        
        res.setCurrentlyIssuedBooks(currentlyIssued);
        res.setReturnedBooks(returned);
        
        long overdue = issues.stream().filter(i -> i.getStatus() == IssueStatus.ISSUED && i.getDueDate().isBefore(LocalDate.now())).count();
        res.setOverdueBooks(overdue);
        
        Integer tf = bookIssueRepository.getTotalFine();
        res.setTotalFine(tf != null ? tf : 0);
        
        return ResponseEntity.ok(res);
    }
}
""",
    "college-library/src/main/resources/static/index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>College Library Management</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        h1, h2 { color: #333; text-align: center; }
        .dashboard { display: flex; gap: 15px; flex-wrap: wrap; justify-content: center; margin-bottom: 20px; }
        .card { background: #007bff; color: white; padding: 20px; border-radius: 8px; text-align: center; width: 150px; font-weight: bold; }
        nav { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; }
        button { padding: 10px 15px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #218838; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f8f9fa; }
        .hidden { display: none; }
        input, select { padding: 8px; margin: 5px 0; width: 100%; box-sizing: border-box; }
        .form-group { margin-bottom: 15px; }
        .action-btn { background: #17a2b8; padding: 5px 10px; margin-right: 5px; }
        .danger-btn { background: #dc3545; }
    </style>
</head>
<body>

<div class="container">
    <h1>College Library Management</h1>
    
    <nav>
        <button onclick="showSection('dashboard-sec'); loadDashboard()">Dashboard</button>
        <button onclick="showSection('books-sec'); loadBooks()">Books</button>
        <button onclick="showSection('students-sec'); loadStudents()">Students</button>
        <button onclick="showSection('issue-sec'); loadIssueData()">Issue/Return Book</button>
    </nav>

    <!-- Dashboard -->
    <div id="dashboard-sec">
        <h2>Dashboard</h2>
        <div class="dashboard" id="dash-cards">
            <!-- Loaded via JS -->
        </div>
    </div>

    <!-- Books -->
    <div id="books-sec" class="hidden">
        <h2>Books Management</h2>
        <button onclick="document.getElementById('book-form').classList.toggle('hidden')">Add New Book</button>
        <input type="text" id="search-book" placeholder="Search by Title, Author, Category..." onkeyup="searchBooks()">
        
        <div id="book-form" class="hidden" style="margin-top: 15px; background: #f9f9f9; padding: 15px; border-radius: 8px;">
            <input type="text" id="b-title" placeholder="Title">
            <input type="text" id="b-author" placeholder="Author">
            <input type="text" id="b-isbn" placeholder="ISBN">
            <input type="text" id="b-cat" placeholder="Category">
            <input type="number" id="b-copies" placeholder="Total Copies">
            <button onclick="saveBook()">Save</button>
        </div>

        <table>
            <thead><tr><th>ID</th><th>Title</th><th>Author</th><th>ISBN</th><th>Category</th><th>Copies</th><th>Available</th></tr></thead>
            <tbody id="books-table"></tbody>
        </table>
    </div>

    <!-- Students -->
    <div id="students-sec" class="hidden">
        <h2>Students Management</h2>
        <button onclick="document.getElementById('student-form').classList.toggle('hidden')">Add New Student</button>
        
        <div id="student-form" class="hidden" style="margin-top: 15px; background: #f9f9f9; padding: 15px; border-radius: 8px;">
            <input type="text" id="s-id" placeholder="Student ID (e.g. CSE001)">
            <input type="text" id="s-name" placeholder="Name">
            <input type="text" id="s-dept" placeholder="Department">
            <input type="number" id="s-year" placeholder="Year">
            <input type="email" id="s-email" placeholder="Email">
            <input type="text" id="s-phone" placeholder="Phone">
            <button onclick="saveStudent()">Save</button>
        </div>

        <table>
            <thead><tr><th>ID</th><th>Student ID</th><th>Name</th><th>Dept</th><th>Year</th><th>Email</th></tr></thead>
            <tbody id="students-table"></tbody>
        </table>
    </div>

    <!-- Issue & Return -->
    <div id="issue-sec" class="hidden">
        <h2>Issue Book</h2>
        <div style="background: #f9f9f9; padding: 15px; border-radius: 8px;">
            <select id="issue-student"><option value="">Select Student</option></select>
            <select id="issue-book"><option value="">Select Book</option></select>
            <button onclick="issueBook()">Issue</button>
        </div>

        <h2>Currently Issued Books</h2>
        <table>
            <thead><tr><th>ID</th><th>Student</th><th>Book</th><th>Issue Date</th><th>Due Date</th><th>Fine</th><th>Action</th></tr></thead>
            <tbody id="issued-table"></tbody>
        </table>
    </div>
</div>

<script>
    const API = 'http://localhost:8080/api';

    function showSection(id) {
        ['dashboard-sec', 'books-sec', 'students-sec', 'issue-sec'].forEach(sec => {
            document.getElementById(sec).classList.add('hidden');
        });
        document.getElementById(id).classList.remove('hidden');
    }

    async function loadDashboard() {
        const res = await fetch(`${API}/dashboard`);
        const data = await res.json();
        document.getElementById('dash-cards').innerHTML = `
            <div class="card">Total Books<br>${data.totalBookRecords}</div>
            <div class="card">Total Copies<br>${data.totalBookCopies}</div>
            <div class="card">Available<br>${data.availableCopies}</div>
            <div class="card">Issued<br>${data.issuedCopies}</div>
            <div class="card">Students<br>${data.totalStudents}</div>
            <div class="card">Overdue<br>${data.overdueBooks}</div>
        `;
    }

    async function loadBooks() {
        const res = await fetch(`${API}/books`);
        const books = await res.json();
        renderBooks(books);
    }

    function renderBooks(books) {
        const tbody = document.getElementById('books-table');
        tbody.innerHTML = books.map(b => `
            <tr>
                <td>${b.id}</td><td>${b.title}</td><td>${b.author}</td>
                <td>${b.isbn}</td><td>${b.category}</td><td>${b.totalCopies}</td>
                <td>${b.availableCopies}</td>
            </tr>
        `).join('');
    }

    async function searchBooks() {
        const q = document.getElementById('search-book').value;
        const res = await fetch(`${API}/books/search?keyword=${q}`);
        renderBooks(await res.json());
    }

    async function saveBook() {
        const book = {
            title: document.getElementById('b-title').value,
            author: document.getElementById('b-author').value,
            isbn: document.getElementById('b-isbn').value,
            category: document.getElementById('b-cat').value,
            totalCopies: document.getElementById('b-copies').value
        };
        await fetch(`${API}/books`, {
            method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(book)
        });
        alert('Book added!');
        loadBooks();
    }

    async function loadStudents() {
        const res = await fetch(`${API}/students`);
        const students = await res.json();
        const tbody = document.getElementById('students-table');
        tbody.innerHTML = students.map(s => `
            <tr>
                <td>${s.id}</td><td>${s.studentId}</td><td>${s.name}</td>
                <td>${s.department}</td><td>${s.year}</td><td>${s.email}</td>
            </tr>
        `).join('');
    }

    async function saveStudent() {
        const student = {
            studentId: document.getElementById('s-id').value,
            name: document.getElementById('s-name').value,
            department: document.getElementById('s-dept').value,
            year: document.getElementById('s-year').value,
            email: document.getElementById('s-email').value,
            phone: document.getElementById('s-phone').value
        };
        await fetch(`${API}/students`, {
            method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(student)
        });
        alert('Student added!');
        loadStudents();
    }

    async function loadIssueData() {
        // Load dropdowns
        const sRes = await fetch(`${API}/students`);
        const sData = await sRes.json();
        document.getElementById('issue-student').innerHTML = `<option value="">Select Student</option>` + 
            sData.map(s => `<option value="${s.id}">${s.name} (${s.studentId})</option>`).join('');

        const bRes = await fetch(`${API}/books`);
        const bData = await bRes.json();
        document.getElementById('issue-book').innerHTML = `<option value="">Select Book</option>` + 
            bData.map(b => `<option value="${b.id}">${b.title} (Avail: ${b.availableCopies})</option>`).join('');

        // Load currently issued
        const iRes = await fetch(`${API}/issues/issued`);
        const iData = await iRes.json();
        document.getElementById('issued-table').innerHTML = iData.map(i => `
            <tr>
                <td>${i.id}</td><td>${i.student.name}</td><td>${i.book.title}</td>
                <td>${i.issueDate}</td><td>${i.dueDate}</td><td>₹${i.fineAmount}</td>
                <td><button class="action-btn danger-btn" onclick="returnBook(${i.id})">Return</button></td>
            </tr>
        `).join('');
    }

    async function issueBook() {
        const sId = document.getElementById('issue-student').value;
        const bId = document.getElementById('issue-book').value;
        if(!sId || !bId) return alert('Select both');
        
        const res = await fetch(`${API}/issues`, {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({studentId: sId, bookId: bId})
        });
        if(res.ok) {
            alert('Issued!');
            loadIssueData();
        } else {
            const err = await res.json();
            alert(err.error || 'Failed');
        }
    }

    async function returnBook(id) {
        const res = await fetch(`${API}/issues/${id}/return`, {method: 'PUT'});
        if(res.ok) {
            alert('Returned!');
            loadIssueData();
        } else {
            const err = await res.json();
            alert(err.error || 'Failed');
        }
    }

    window.onload = loadDashboard;
</script>
</body>
</html>
""",
    "college-library/README.md": """# College Library Management System

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
"""
}

for path, content in code_files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Generated complete Spring Boot codebase successfully.")
