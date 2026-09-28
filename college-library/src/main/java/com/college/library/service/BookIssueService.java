package com.college.library.service;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.college.library.entity.Book;
import com.college.library.entity.BookIssue;
import com.college.library.entity.IssueStatus;
import com.college.library.entity.Student;
import com.college.library.exception.BadRequestException;
import com.college.library.exception.ResourceNotFoundException;
import com.college.library.repository.BookIssueRepository;
import com.college.library.repository.BookRepository;
import com.college.library.repository.StudentRepository;

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
        return issueBook(studentId, bookId, null);
    }

    @Transactional
    public BookIssue issueBook(Long studentId, Long bookId, LocalDate customIssueDate) {
        Student student = studentRepository.findById(studentId)
                .orElseThrow(() -> new ResourceNotFoundException("Student not found"));
        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found"));

        if (book.getAvailableCopies() <= 0) {
            throw new BadRequestException("No copies of this book are currently available.");
        }

        book.setAvailableCopies(book.getAvailableCopies() - 1);
        bookRepository.save(book);

        LocalDate issueDate = customIssueDate != null ? customIssueDate : LocalDate.now();

        BookIssue issue = new BookIssue();
        issue.setStudent(student);
        issue.setBook(book);
        issue.setIssueDate(issueDate);
        issue.setDueDate(issueDate.plusDays(ISSUE_DAYS));
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
        issue.setFineAmount(calculateFine(issue.getIssueDate(), issue.getReturnDate()));

        Book book = issue.getBook();
        book.setAvailableCopies(book.getAvailableCopies() + 1);
        bookRepository.save(book);

        return bookIssueRepository.save(issue);
    }
    
    public int calculateFine(LocalDate issueDate, LocalDate calculationDate) {
        long daysNotReturned = ChronoUnit.DAYS.between(issueDate, calculationDate);
        return (int) Math.max(0, daysNotReturned) * FINE_PER_DAY;
    }

    public List<BookIssue> getCurrentlyIssuedBooksByStudent(Long studentId) {
        List<BookIssue> issues = bookIssueRepository.findByStudentIdAndStatus(studentId, IssueStatus.ISSUED);
        issues.forEach(i -> i.setFineAmount(calculateFine(i.getIssueDate(), LocalDate.now())));
        return issues;
    }

    public List<BookIssue> getStudentHistory(Long studentId) {
        return bookIssueRepository.findByStudentId(studentId);
    }

    public List<BookIssue> getAllIssuedBooks() {
        List<BookIssue> issues = bookIssueRepository.findByStatus(IssueStatus.ISSUED);
        issues.forEach(i -> i.setFineAmount(calculateFine(i.getIssueDate(), LocalDate.now())));
        return issues;
    }
}
