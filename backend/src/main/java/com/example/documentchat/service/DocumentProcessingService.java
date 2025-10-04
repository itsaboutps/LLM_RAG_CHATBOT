package com.example.documentchat.service;

import com.example.documentchat.model.Document;
import com.example.documentchat.model.DocumentChunk;
import com.example.documentchat.repository.DocumentChunkRepository;
import com.example.documentchat.repository.DocumentRepository;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFParagraph;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

@Service
public class DocumentProcessingService {
    
    @Autowired
    private DocumentRepository documentRepository;
    
    @Autowired
    private DocumentChunkRepository documentChunkRepository;
    
    @Autowired
    private EmbeddingService embeddingService;
    
    public Document processDocument(MultipartFile file) throws IOException {
        String fileName = file.getOriginalFilename();
        String fileType = getFileType(fileName);
        String extractedText = extractTextFromFile(file, fileType);
        
        Document document = new Document(fileName, fileType, file.getSize(), extractedText);
        document = documentRepository.save(document);
        
        // Split text into chunks and create embeddings
        List<String> chunks = splitTextIntoChunks(extractedText);
        List<DocumentChunk> documentChunks = new ArrayList<>();
        
        for (int i = 0; i < chunks.size(); i++) {
            String chunkText = chunks.get(i);
            float[] embedding = embeddingService.generateEmbedding(chunkText);
            
            DocumentChunk documentChunk = new DocumentChunk(document, chunkText, i, embedding);
            documentChunks.add(documentChunk);
        }
        
        documentChunkRepository.saveAll(documentChunks);
        document.setChunks(documentChunks);
        
        return document;
    }
    
    private String getFileType(String fileName) {
        if (fileName == null) return "unknown";
        String extension = fileName.substring(fileName.lastIndexOf(".") + 1).toLowerCase();
        return switch (extension) {
            case "pdf" -> "application/pdf";
            case "docx" -> "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
            case "txt" -> "text/plain";
            default -> "unknown";
        };
    }
    
    private String extractTextFromFile(MultipartFile file, String fileType) throws IOException {
        try (InputStream inputStream = file.getInputStream()) {
            return switch (fileType) {
                case "application/pdf" -> extractTextFromPDF(inputStream);
                case "application/vnd.openxmlformats-officedocument.wordprocessingml.document" -> extractTextFromDOCX(inputStream);
                case "text/plain" -> new String(inputStream.readAllBytes());
                default -> throw new IllegalArgumentException("Unsupported file type: " + fileType);
            };
        }
    }
    
    private String extractTextFromPDF(InputStream inputStream) throws IOException {
        try (PDDocument document = PDDocument.load(inputStream)) {
            PDFTextStripper stripper = new PDFTextStripper();
            return stripper.getText(document);
        }
    }
    
    private String extractTextFromDOCX(InputStream inputStream) throws IOException {
        try (XWPFDocument document = new XWPFDocument(inputStream)) {
            StringBuilder text = new StringBuilder();
            for (XWPFParagraph paragraph : document.getParagraphs()) {
                text.append(paragraph.getText()).append("\n");
            }
            return text.toString();
        }
    }
    
    private List<String> splitTextIntoChunks(String text) {
        List<String> chunks = new ArrayList<>();
        int chunkSize = 1000; // characters per chunk
        int overlap = 200; // overlap between chunks
        
        for (int i = 0; i < text.length(); i += chunkSize - overlap) {
            int end = Math.min(i + chunkSize, text.length());
            String chunk = text.substring(i, end).trim();
            if (!chunk.isEmpty()) {
                chunks.add(chunk);
            }
        }
        
        return chunks;
    }
    
    public List<Document> getAllDocuments() {
        return documentRepository.findAll();
    }
    
    public void deleteDocument(Long documentId) {
        documentRepository.deleteById(documentId);
    }
}
