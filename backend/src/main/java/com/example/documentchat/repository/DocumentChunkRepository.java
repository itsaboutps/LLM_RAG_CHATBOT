package com.example.documentchat.repository;

import com.example.documentchat.model.DocumentChunk;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DocumentChunkRepository extends JpaRepository<DocumentChunk, Long> {
    
    @Query("SELECT dc FROM DocumentChunk dc WHERE dc.document.id = :documentId ORDER BY dc.chunkIndex")
    List<DocumentChunk> findByDocumentIdOrderByChunkIndex(@Param("documentId") Long documentId);
    
    @Query("SELECT dc FROM DocumentChunk dc")
    List<DocumentChunk> findAllChunks();
}
