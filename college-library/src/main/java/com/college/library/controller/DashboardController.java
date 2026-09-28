package com.college.library.controller;

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
