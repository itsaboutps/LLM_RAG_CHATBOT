package com.example.documentchat.controller;

import com.example.documentchat.model.Document;
import com.example.documentchat.service.DocumentProcessingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api/documents")
@CrossOrigin(origins = "http://localhost:4200")
public class DocumentController {
    
    @Autowired
    private DocumentProcessingService documentProcessingService;
    
    @PostMapping("/upload")
    public ResponseEntity<Document> uploadDocument(@RequestParam("file") MultipartFile file) {
        try {
            if (file.isEmpty()) {
                return ResponseEntity.badRequest().build();
            }
            
            String fileName = file.getOriginalFilename();
            if (fileName == null || (!fileName.toLowerCase().endsWith(".pdf") && 
                                   !fileName.toLowerCase().endsWith(".docx") && 
                                   !fileName.toLowerCase().endsWith(".txt"))) {
                return ResponseEntity.badRequest().build();
            }
            
            Document document = documentProcessingService.processDocument(file);
            return ResponseEntity.ok(document);
        } catch (IOException e) {
            return ResponseEntity.internalServerError().build();
        }
    }
    
    @GetMapping
    public ResponseEntity<List<Document>> getAllDocuments() {
        List<Document> documents = documentProcessingService.getAllDocuments();
        return ResponseEntity.ok(documents);
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteDocument(@PathVariable Long id) {
        documentProcessingService.deleteDocument(id);
        return ResponseEntity.ok().build();
    }
}
