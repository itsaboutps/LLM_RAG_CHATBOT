package com.example.documentchat.model;

import java.time.LocalDateTime;

public class ChatMessage {
    private String message;
    private String response;
    private LocalDateTime timestamp;
    private String source; // "documents" or "out_of_scope" or "no_documents"
    
    public ChatMessage() {}
    
    public ChatMessage(String message, String response, String source) {
        this.message = message;
        this.response = response;
        this.source = source;
        this.timestamp = LocalDateTime.now();
    }
    
    // Getters and Setters
    public String getMessage() {
        return message;
    }
    
    public void setMessage(String message) {
        this.message = message;
    }
    
    public String getResponse() {
        return response;
    }
    
    public void setResponse(String response) {
        this.response = response;
    }
    
    public LocalDateTime getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }
    
    public String getSource() {
        return source;
    }
    
    public void setSource(String source) {
        this.source = source;
    }
}
