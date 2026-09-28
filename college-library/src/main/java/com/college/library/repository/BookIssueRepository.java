package com.college.library.repository;

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
