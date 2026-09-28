package com.college.library;

import java.time.LocalDate;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import com.college.library.entity.Book;
import com.college.library.entity.BookIssue;
import com.college.library.entity.IssueStatus;
import com.college.library.entity.Student;
import com.college.library.exception.BadRequestException;
import com.college.library.repository.BookIssueRepository;
import com.college.library.repository.BookRepository;
import com.college.library.repository.StudentRepository;
import com.college.library.service.BookIssueService;
import com.college.library.service.BookService;
import com.college.library.service.StudentService;

@SpringBootTest
@Transactional
@ActiveProfiles("test") // Allows for H2 config if needed, or runs on MySQL
class CollegeLibraryApplicationTests {

    @Autowired private BookService bookService;
    @Autowired private StudentService studentService;
    @Autowired private BookIssueService bookIssueService;
    
    @Autowired private BookRepository bookRepository;
    @Autowired private StudentRepository studentRepository;
    @Autowired private BookIssueRepository bookIssueRepository;

    private Book savedBook;
    private Student savedStudent;

    @BeforeEach
    void setUp() {
        Book book = new Book();
        book.setTitle("Test Book");
        book.setAuthor("Test Author");
        book.setIsbn("1234567890");
        book.setCategory("Science");
        book.setTotalCopies(2);
        savedBook = bookService.addBook(book);

        Student student = new Student();
        student.setStudentId("STU001");
        student.setName("Test Student");
        student.setDepartment("CS");
        student.setYear(2);
        student.setEmail("test@student.com");
        student.setPhone("1234567890");
        savedStudent = studentService.addStudent(student);
    }

    @Test
    void testCreateAndGetBook() {
        Book found = bookService.getBookById(savedBook.getId());
        assertEquals("Test Book", found.getTitle());
        assertEquals(2, found.getAvailableCopies());
    }

    @Test
    void testIssueBook() {
        BookIssue issue = bookIssueService.issueBook(savedStudent.getId(), savedBook.getId());
        assertNotNull(issue.getId());
        assertEquals(IssueStatus.ISSUED, issue.getStatus());
        assertEquals(1, bookRepository.findById(savedBook.getId()).get().getAvailableCopies());
        assertEquals(LocalDate.now(), issue.getIssueDate());
        assertEquals(LocalDate.now().plusDays(14), issue.getDueDate());
    }

    @Test
    void testRejectIssueWhenNoCopies() {
        bookIssueService.issueBook(savedStudent.getId(), savedBook.getId());
        
        Student student2 = new Student();
        student2.setStudentId("STU002");
        student2.setName("Test Student 2");
        student2.setDepartment("CS");
        student2.setYear(2);
        student2.setEmail("test2@student.com");
        student2.setPhone("1234567891");
        Student savedStudent2 = studentService.addStudent(student2);
        
        bookIssueService.issueBook(savedStudent2.getId(), savedBook.getId());
        
        // No copies left
        Student student3 = new Student();
        student3.setStudentId("STU003");
        student3.setName("Test Student 3");
        student3.setDepartment("CS");
        student3.setYear(2);
        student3.setEmail("test3@student.com");
        student3.setPhone("1234567892");
        Student savedStudent3 = studentService.addStudent(student3);
        
        assertThrows(BadRequestException.class, () -> {
            bookIssueService.issueBook(savedStudent3.getId(), savedBook.getId());
        });
    }

    @Test
    void testReturnBook() {
        BookIssue issue = bookIssueService.issueBook(savedStudent.getId(), savedBook.getId(), LocalDate.now().minusDays(3));
        assertEquals(1, bookRepository.findById(savedBook.getId()).get().getAvailableCopies());
        
        BookIssue returnedIssue = bookIssueService.returnBook(issue.getId());
        assertEquals(IssueStatus.RETURNED, returnedIssue.getStatus());
        assertEquals(2, bookRepository.findById(savedBook.getId()).get().getAvailableCopies());
        assertEquals(30, returnedIssue.getFineAmount());
    }

    @Test
    void testFineCalculation() {
        int fine0 = bookIssueService.calculateFine(LocalDate.now(), LocalDate.now());
        assertEquals(0, fine0);

        int fine1 = bookIssueService.calculateFine(LocalDate.now().minusDays(1), LocalDate.now());
        assertEquals(10, fine1);

        int fine14 = bookIssueService.calculateFine(LocalDate.now().minusDays(14), LocalDate.now());
        assertEquals(140, fine14);

        int fineForFutureIssue = bookIssueService.calculateFine(LocalDate.now().plusDays(1), LocalDate.now());
        assertEquals(0, fineForFutureIssue);

        int leapYearFine = bookIssueService.calculateFine(LocalDate.of(2024, 2, 28), LocalDate.of(2024, 3, 1));
        assertEquals(20, leapYearFine);

        int nonLeapYearFine = bookIssueService.calculateFine(LocalDate.of(2025, 2, 28), LocalDate.of(2025, 3, 1));
        assertEquals(10, nonLeapYearFine);
    }
    
    @Test
    void testStudentHistory() {
        bookIssueService.issueBook(savedStudent.getId(), savedBook.getId());
        List<BookIssue> issues = bookIssueService.getCurrentlyIssuedBooksByStudent(savedStudent.getId());
        assertEquals(1, issues.size());
    }
}
