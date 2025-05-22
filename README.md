# PDF Chat Application

This is a full-stack application that allows users to chat with their PDF documents using Google's Gemini AI model. The application uses a Streamlit frontend and a Flask backend with advanced document processing capabilities.

## Features

- PDF document processing and indexing
- Semantic search using FAISS (Facebook AI Similarity Search)
- Image captioning using Gemini AI
- Real-time chat interface
- Document chunking and semantic merging
- Support for multiple document formats (PDF, HTML, text)
- Efficient document caching and indexing

## Project Structure
```
.
├── frontend/
│   ├── app.py              # Streamlit frontend application
│   └── requirements.txt    # Frontend dependencies
├── backend/
│   ├── app.py             # Flask backend server
│   ├── main.py            # Core document processing logic
│   ├── requirements.txt   # Backend dependencies
│   ├── documents/         # Directory for uploaded documents
│   │   └── images/       # Directory for extracted images
│   └── faiss_index/      # Directory for document indices
└── README.md
```

## Prerequisites

- Python 3.10 or higher
- Google Cloud account with Gemini API access
- CUDA-compatible GPU (optional, for better performance)

## Backend Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the backend directory with:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   ```

4. Create required directories:
   ```bash
   mkdir -p documents/images
   mkdir -p faiss_index
   ```

5. Run the backend server:
   ```bash
   python app.py
   ```

## Frontend Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd frontend
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the frontend directory with:
   ```
   BACKEND_URL=http://localhost:5000
   ```

4. Run the frontend:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Upload PDF documents through the frontend interface
2. The backend will automatically:
   - Extract text and images from PDFs
   - Generate captions for images
   - Create semantic chunks of the content
   - Build a FAISS index for efficient searching
3. Use the chat interface to ask questions about your documents
4. The system will:
   - Search for relevant document chunks
   - Use Gemini AI to generate contextual responses
   - Present the information in a readable format

## Technical Details

- **Document Processing**: Uses `pymupdf4llm` for PDF extraction and `trafilatura` for web content
- **Vector Search**: Implements FAISS for efficient similarity search
- **AI Integration**: Uses Google's Gemini model for:
  - Text embeddings
  - Image captioning
  - Response generation
- **Caching**: Implements document caching to avoid reprocessing unchanged files
- **Error Handling**: Comprehensive error handling and logging

## Security Considerations

1. Keep your Gemini API key secure
2. Implement proper authentication for production use
3. Use HTTPS in production
4. Set up proper CORS policies
5. Implement rate limiting
6. Regular security updates

## Troubleshooting

1. If FAISS installation fails:
   - Install SWIG: `sudo apt-get install swig`
   - Try installing CPU version: `pip install faiss-cpu`

2. If document processing fails:
   - Check file permissions
   - Ensure sufficient disk space
   - Verify document format compatibility

3. If API calls fail:
   - Verify API key
   - Check network connectivity
   - Monitor API rate limits

## Contributing

Feel free to submit issues and enhancement requests! 