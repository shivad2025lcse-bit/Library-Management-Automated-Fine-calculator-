package com.college.library.controller;

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
        return ResponseEntity.ok(bookIssueService.issueBook(request.getStudentId(), request.getBookId(), request.getIssueDate()));
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
