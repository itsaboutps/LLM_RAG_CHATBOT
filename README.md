<<<<<<< HEAD
# LLM_RAG_CHATBOT
=======
# Document Chat Application

A complete end-to-end web application that allows users to chat with an AI assistant restricted only to the documents they upload. Built with Angular frontend, Spring Boot backend, and Gemini Pro API.

## Features

- **Document Upload**: Support for PDF, DOCX, and TXT files
- **Text Extraction**: Automatic text extraction from uploaded documents
- **Vector Search**: Document chunks are embedded and stored for semantic search
- **AI Chat**: Chat interface that answers only from uploaded documents
- **Smart Responses**: 
  - Answers from documents when relevant
  - "Out of scope" for unrelated questions
  - "No documents available" when no documents are uploaded
  - Highlights conflicts when documents contain conflicting information

## Tech Stack

- **Frontend**: Angular 17
- **Backend**: Spring Boot 3.2.0
- **Database**: H2 (in-memory)
- **AI**: Google Gemini Pro API
- **Document Processing**: Apache PDFBox, Apache POI
- **Vector Storage**: Custom implementation with cosine similarity

## Quick Start

### Prerequisites

- Java 17 or higher
- Node.js 18 or higher
- npm or yarn
- Google Gemini API key (optional - app works without it using dummy responses)

### 1. Backend Setup

```bash
cd backend
./mvnw spring-boot:run
```

The backend will start on `http://localhost:8080`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm start
```

The frontend will start on `http://localhost:4200`

### 3. Configure Gemini API (Required for AI Responses)

**⚠️ IMPORTANT**: The application requires a Gemini API key to work properly. Without it, you'll get dummy responses.

#### Quick Setup:
```bash
./setup-api-key.sh
```

#### Manual Setup:

1. **Get your API key**:
   - Go to: https://makersuite.google.com/app/apikey
   - Create a new API key
   - Copy the API key

2. **Set the API key** (choose one method):

   **Option A - Environment Variable (Recommended)**:
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

   **Option B - Add to application.properties**:
   ```properties
   gemini.api.key=your_api_key_here
   ```

   **Option C - Set temporarily for testing**:
   ```bash
   GEMINI_API_KEY=your_api_key_here ./start-backend.sh
   ```

3. **Restart the backend** after setting the API key:
   ```bash
   cd backend && mvn spring-boot:run
   ```

## How It Works

1. **Document Upload**: Users upload PDF, DOCX, or TXT files through the web interface
2. **Text Extraction**: Backend extracts text from documents using Apache PDFBox and POI
3. **Chunking**: Text is split into manageable chunks (1000 characters with 200 character overlap)
4. **Embedding**: Each chunk is converted to a vector embedding using Gemini's embedding API
5. **Storage**: Embeddings are stored in the database with the original text
6. **Query Processing**: When users ask questions:
   - Query is converted to an embedding
   - Similar chunks are found using cosine similarity
   - Relevant context is sent to Gemini Pro for response generation
   - Response is returned with source information

## API Endpoints

### Documents
- `POST /api/documents/upload` - Upload a document
- `GET /api/documents` - Get all documents
- `DELETE /api/documents/{id}` - Delete a document

### Chat
- `POST /api/chat/message` - Send a chat message

## Configuration

### Backend Configuration (`application.properties`)

```properties
# Server
server.port=8080

# Database
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.username=sa
spring.datasource.password=password

# File upload
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB

# Gemini API
gemini.api.key=${GEMINI_API_KEY:}
```

## Development

### Backend Development

```bash
cd backend
./mvnw spring-boot:run
```

### Frontend Development

```bash
cd frontend
npm start
```

### Building for Production

Backend:
```bash
cd backend
./mvnw clean package
java -jar target/document-chat-backend-0.0.1-SNAPSHOT.jar
```

Frontend:
```bash
cd frontend
npm run build
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `application.properties`
2. **CORS errors**: Ensure the frontend URL is correct in the CORS configuration
3. **File upload fails**: Check file size limits and supported formats
4. **No AI responses or "Out of scope" for valid questions**: 
   - **Most common cause**: Missing or invalid Gemini API key
   - Run `./setup-api-key.sh` to check your API key setup
   - Verify the API key is set: `echo $GEMINI_API_KEY`
   - Restart the backend after setting the API key
5. **Poor response quality**: The dummy embedding system has limitations; use a real Gemini API key for better results

### Logs

Backend logs are available in the console. For more detailed logging, modify `logback-spring.xml`.

## License

This project is for educational purposes. Please ensure you comply with Google's Gemini API terms of service when using the AI features.
>>>>>>> 0822860 (RAG Chatbot)
