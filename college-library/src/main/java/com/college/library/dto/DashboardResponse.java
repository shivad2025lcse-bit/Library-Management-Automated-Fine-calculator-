package com.college.library.dto;

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
