package com.example.documentchat.model;

import jakarta.persistence.*;
import java.util.Arrays;

@Entity
@Table(name = "document_chunks")
public class DocumentChunk {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "document_id", nullable = false)
    private Document document;
    
    @Column(columnDefinition = "TEXT")
    private String text;
    
    @Column(nullable = false)
    private int chunkIndex;
    
    @Column(columnDefinition = "TEXT")
    private String embedding; // JSON string of float array
    
    // Constructors
    public DocumentChunk() {}
    
    public DocumentChunk(Document document, String text, int chunkIndex, float[] embedding) {
        this.document = document;
        this.text = text;
        this.chunkIndex = chunkIndex;
        this.embedding = arrayToString(embedding);
    }
    
    // Helper methods for embedding conversion
    public float[] getEmbeddingAsArray() {
        return stringToArray(this.embedding);
    }
    
    public void setEmbeddingFromArray(float[] embedding) {
        this.embedding = arrayToString(embedding);
    }
    
    private String arrayToString(float[] array) {
        if (array == null) return null;
        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for (int i = 0; i < array.length; i++) {
            if (i > 0) sb.append(",");
            sb.append(array[i]);
        }
        sb.append("]");
        return sb.toString();
    }
    
    private float[] stringToArray(String str) {
        if (str == null || str.trim().isEmpty()) return null;
        str = str.trim();
        if (str.startsWith("[") && str.endsWith("]")) {
            str = str.substring(1, str.length() - 1);
        }
        String[] parts = str.split(",");
        float[] result = new float[parts.length];
        for (int i = 0; i < parts.length; i++) {
            result[i] = Float.parseFloat(parts[i].trim());
        }
        return result;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public Document getDocument() {
        return document;
    }
    
    public void setDocument(Document document) {
        this.document = document;
    }
    
    public String getText() {
        return text;
    }
    
    public void setText(String text) {
        this.text = text;
    }
    
    public int getChunkIndex() {
        return chunkIndex;
    }
    
    public void setChunkIndex(int chunkIndex) {
        this.chunkIndex = chunkIndex;
    }
    
    public String getEmbedding() {
        return embedding;
    }
    
    public void setEmbedding(String embedding) {
        this.embedding = embedding;
    }
}
