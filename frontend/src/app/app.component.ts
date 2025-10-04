import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

interface Document {
  id: number;
  fileName: string;
  fileType: string;
  fileSize: number;
  uploadTime: string;
}

interface ChatMessage {
  message: string;
  response: string;
  timestamp: string;
  source: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  documents: Document[] = [];
  messages: ChatMessage[] = [];
  newMessage: string = '';
  isLoading: boolean = false;
  selectedFile: File | null = null;
  statusMessage: string = '';
  statusType: 'success' | 'error' | '' = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadDocuments();
    // Load documents every 2 seconds to keep UI updated
    setInterval(() => {
      this.loadDocuments();
    }, 2000);
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.uploadFile();
    }
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.selectedFile = files[0];
      this.uploadFile();
    }
  }

  uploadFile() {
    if (!this.selectedFile) return;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post<Document>('http://localhost:8080/api/documents/upload', formData)
      .subscribe({
        next: (uploadedDocument) => {
          this.documents.push(uploadedDocument);
          this.showStatus('Document uploaded successfully!', 'success');
          this.selectedFile = null;
          // Reset file input
          const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
          if (fileInput) fileInput.value = '';
        },
        error: (error) => {
          console.error('Upload error:', error);
          this.showStatus('Error uploading document. Please try again.', 'error');
        }
      });
  }

  deleteDocument(id: number) {
    this.http.delete(`http://localhost:8080/api/documents/${id}`)
      .subscribe({
        next: () => {
          this.documents = this.documents.filter(doc => doc.id !== id);
          this.showStatus('Document deleted successfully!', 'success');
        },
        error: (error) => {
          console.error('Delete error:', error);
          this.showStatus('Error deleting document.', 'error');
        }
      });
  }

  sendMessage() {
    if (!this.newMessage.trim()) return;

    const userMessage: ChatMessage = {
      message: this.newMessage,
      response: '',
      timestamp: new Date().toISOString(),
      source: 'user'
    };

    this.messages.push(userMessage);
    const currentMessage = this.newMessage;
    this.newMessage = '';
    this.isLoading = true;

    this.http.post<ChatMessage>('http://localhost:8080/api/chat/message', { message: currentMessage })
      .subscribe({
        next: (response) => {
          this.messages.push(response);
          this.isLoading = false;
        },
        error: (error) => {
          console.error('Chat error:', error);
          this.messages.push({
            message: '',
            response: 'Sorry, there was an error processing your request.',
            timestamp: new Date().toISOString(),
            source: 'error'
          });
          this.isLoading = false;
        }
      });
  }

  loadDocuments() {
    this.http.get<Document[]>('http://localhost:8080/api/documents')
      .subscribe({
        next: (documents) => {
          this.documents = documents;
        },
        error: (error) => {
          console.error('Error loading documents:', error);
        }
      });
  }

  showStatus(message: string, type: 'success' | 'error') {
    this.statusMessage = message;
    this.statusType = type;
    setTimeout(() => {
      this.statusMessage = '';
      this.statusType = '';
    }, 3000);
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleString();
  }

  getMessageClass(source: string): string {
    switch (source) {
      case 'user': return 'user';
      case 'documents': return 'assistant';
      case 'out_of_scope': return 'out-of-scope';
      case 'no_documents': return 'no-documents';
      default: return 'assistant';
    }
  }

  getSourceText(source: string): string {
    switch (source) {
      case 'user': return 'You';
      case 'documents': return 'AI Assistant (from documents)';
      case 'out_of_scope': return 'AI Assistant (out of scope)';
      case 'no_documents': return 'AI Assistant (no documents)';
      default: return 'AI Assistant';
    }
  }

  getFileTypeDisplay(fileType: string): string {
    if (fileType.includes('pdf')) return 'PDF Document';
    if (fileType.includes('word') || fileType.includes('document')) return 'Word Document';
    if (fileType.includes('text')) return 'Text File';
    return 'Document';
  }
}
