package com.college.library.dto;

public class IssueBookRequest {
    private Long studentId;
    private Long bookId;
    private java.time.LocalDate issueDate;

    public Long getStudentId() { return studentId; }
    public void setStudentId(Long studentId) { this.studentId = studentId; }
    public Long getBookId() { return bookId; }
    public void setBookId(Long bookId) { this.bookId = bookId; }
    public java.time.LocalDate getIssueDate() { return issueDate; }
    public void setIssueDate(java.time.LocalDate issueDate) { this.issueDate = issueDate; }
}
