package com.example.documentchat.controller;

import com.example.documentchat.model.ChatMessage;
import com.example.documentchat.service.ChatService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/chat")
@CrossOrigin(origins = "http://localhost:4200")
public class ChatController {
    
    @Autowired
    private ChatService chatService;
    
    @PostMapping("/message")
    public ResponseEntity<ChatMessage> sendMessage(@RequestBody ChatMessage message) {
        ChatMessage response = chatService.processQuery(message.getMessage());
        return ResponseEntity.ok(response);
    }
}
