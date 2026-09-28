package com.college.library.service;

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
