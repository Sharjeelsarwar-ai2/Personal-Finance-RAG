# FinanceRAG

FinanceRAG is a Streamlit application for asking questions about financial documents. It combines document ingestion, retrieval-augmented generation, source-aware answers, persistent chat memory, conversation exports, and a glassmorphic user interface.

> FinanceRAG is designed to help users explore uploaded documents. It does not replace professional financial, legal, tax, or investment advice.

## Features

FinanceRAG provides a focused workspace for uploading and querying financial documents. Supported document types are **PDF**, **CSV**, **XLSX**, **TXT**, and **DOCX**, provided that the corresponding parsers are implemented in the project’s document-processing layer.

The application processes uploaded files through an ingestion pipeline that extracts text, divides documents into retrieval chunks, creates embeddings, and builds a searchable index. The query console then retrieves relevant context and sends it to the configured language model to generate an answer.

The interface includes a glassmorphic dark theme, responsive layout, document status indicators, an ingestion pipeline visualization, indexed-file search, document preview dialogs, source references, and custom user and assistant chat bubbles.

| Capability | Description |
|---|---|
| Document ingestion | Upload multiple financial documents in one operation. |
| Retrieval pipeline | Extract, chunk, embed, and index document content. |
| Query console | Ask natural-language questions about indexed documents. |
| Source references | Display retrieved source names with assistant responses. |
| Document filtering | Search indexed files by filename or file type. |
| Document preview | Open extracted text in a read-only preview dialog. |
| Chat persistence | Save and restore the conversation from `chat_memory.json`. |
| Markdown export | Download the conversation as a Markdown transcript. |
| PDF export | Download a dependency-free PDF transcript. |
| Responsive UI | Adapt the workspace for desktop and mobile viewports. |

## Application workflow

The application follows this sequence:

1. The user opens the Streamlit application and configures the model connection from **Settings**.
2. The user uploads one or more documents in the **Source library**.
3. `DocumentProcessor` extracts readable text from each file.
4. `RAGEngine` chunks the extracted content, creates embeddings, and builds the retrieval index.
5. The user opens the **Query console** and submits a question.
6. `RAGEngine.query()` retrieves relevant context and returns an answer with sources.
7. The conversation is saved locally and can be downloaded as Markdown or PDF.

## Project structure

The repository should contain the following files:

```text
FinanceRAG/
├── app.py                    # Streamlit entry point and application workflow
├── ui_components.py          # Glassmorphic styling and reusable UI primitives
├── document_processor.py     # File parsing and text extraction layer
├── rag_engine.py             # Chunking, embeddings, indexing, and querying layer
├── requirements.txt          # Python dependencies
├── chat_memory.json          # Runtime-generated local chat history, if enabled
└── README.md                 # Project documentation
```

The current application imports `DocumentProcessor` from `document_processor.py` and `RAGEngine` from `rag_engine.py`. These modules must be present in the same project directory as `app.py` when deploying the application.

## Requirements

Use Python 3.9 or newer. The exact dependency list depends on the implementation of `document_processor.py` and `rag_engine.py`. At minimum, the project requires Streamlit and the libraries used by those backend modules.

A minimal starting `requirements.txt` is:

```text
streamlit
```

Add the libraries required by the backend implementation. Typical projects may also require packages for PDF parsing, spreadsheet handling, embeddings, vector indexing, and the selected LLM provider. Do not add packages that the backend does not import, because unnecessary dependencies can make deployment slower and less reliable.

## Local installation

Clone the repository and create an isolated virtual environment:

```bash
git clone <your-repository-url>
cd FinanceRAG
python -m venv .venv
```

Activate the environment on Linux or macOS:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Start the application:

```bash
streamlit run app.py
```

Streamlit normally opens the application at `http://localhost:8501`.

## Configuration

Open the **Settings** control in the application and enter the API key required by the configured `RAGEngine` implementation. Select the desired model from the available model list.

The current UI includes the following model names:

| Model | Configuration value |
|---|---|
| OpenAI GPT OSS 120B | `openai/gpt-oss-120b` |
| Llama 3.3 70B Versatile | `llama-3.3-70b-versatile` |
| Llama 3.1 8B Instant | `llama-3.1-8b-instant` |
| Mixtral 8x7B | `mixtral-8x7b-32768` |

The selected model must be supported by the backend service used in `rag_engine.py`. If the backend uses an environment variable instead of the in-app settings field, configure that variable according to the backend implementation and deployment provider.

## Using the application

### Upload and index documents

Open **Source library**, select one or more supported files, and choose **Process & index documents**. The application displays progress while it extracts content and builds the retrieval index.

After successful indexing, the Knowledge Base section displays the number of indexed documents and retrieval chunks. The pipeline status changes to **Ready**.

### Search indexed documents

Use the search field above the indexed-file list to filter files by filename or file type. The filter updates the visible file cards and reports how many documents match the current query.

### Preview a document

Choose **Preview** beside an indexed file. FinanceRAG opens a read-only dialog containing the extracted text. The preview is limited to the first 30,000 characters to keep the dialog responsive for large documents.

### Ask questions

Open **Query console** and submit a question in the chat composer. The application sends recent conversation context to `RAGEngine.query()` and displays the generated answer with up to three referenced sources.

## Chat memory

The application stores chat messages in `chat_memory.json` next to `app.py`. The file is loaded during application startup and messages are saved after user and assistant responses.

The memory file is intentionally limited to conversation messages. It does not store the API key. The **Reset** control clears the Streamlit session state and removes the local memory file.

Local file persistence is suitable for a single-user local deployment or a host with persistent disk storage. Streamlit Cloud and similar hosted environments may use ephemeral filesystems. A local JSON file should therefore not be treated as durable production storage.

For guaranteed persistence across redeployments, multiple users, or multiple application instances, replace the JSON storage functions with a database-backed repository. Suitable options include PostgreSQL, Supabase, Firebase, or another persistent datastore. A production implementation should also associate conversations with authenticated users and apply appropriate access controls.

## Conversation exports

When a conversation exists, the Query Console provides two export controls:

- **Export Markdown** creates `financerag-conversation.md` with the conversation, export time, and source references.
- **Export PDF** creates `financerag-conversation.pdf` using a lightweight built-in PDF writer.

The current PDF exporter creates a single-page text transcript and limits the rendered content to the first 110 wrapped lines. For long-form production reports, replace it with a paginated PDF library such as ReportLab or a server-side document-generation service.

## Architecture

The application is divided into three functional layers:

| Layer | Module | Responsibility |
|---|---|---|
| Presentation | `ui_components.py` | CSS theme, layout primitives, chat bubbles, file cards, pipeline, and preview styling. |
| Application | `app.py` | Streamlit configuration, session state, upload flow, chat flow, filtering, persistence, and export actions. |
| Retrieval backend | `document_processor.py`, `rag_engine.py` | File extraction, chunking, embeddings, indexing, retrieval, and answer generation. |

`app.py` imports the presentation layer as a module namespace so UI changes remain centralized and import mismatches produce a clearer startup error. The application keeps temporary runtime objects such as `DocumentProcessor` and `RAGEngine` in `st.session_state`.

## Deployment on Streamlit Cloud

Push all required files to the repository, including `app.py`, `ui_components.py`, `document_processor.py`, `rag_engine.py`, and `requirements.txt`. In Streamlit Cloud, set the main file to `app.py`.

Configure secrets through the platform’s secret manager rather than committing API keys to Git. The exact secret name must match the backend implementation. Never commit API keys, access tokens, private documents, or `chat_memory.json` containing sensitive conversation data.

A recommended `.gitignore` entry is:

```gitignore
.venv/
__pycache__/
*.py[cod]
chat_memory.json
.env
.streamlit/secrets.toml
```

After deployment, verify the following behaviors:

1. The application starts without an import error.
2. The Settings control accepts the configured API key.
3. A small test document can be uploaded and indexed.
4. The pipeline reaches the Ready state.
5. A query returns an answer and source references.
6. The document preview opens successfully.
7. Markdown and PDF exports download successfully.
8. The deployment’s storage behavior is understood before relying on chat memory for important records.

## Security and privacy considerations

Uploaded financial documents and generated answers may contain sensitive information. Use a trusted deployment environment and restrict access to the application whenever confidential data is processed.

Do not log API keys or full document contents unnecessarily. Avoid exposing raw exception details to end users. If the application is deployed for multiple users, implement authentication, user-scoped document indexes, user-scoped conversations, and server-side authorization before processing private files.

The current local chat-memory implementation is not an access-control system. Anyone with access to the deployed filesystem may be able to read the stored JSON file. Use database encryption, access controls, and retention policies for production workloads.

## Troubleshooting

### `ImportError` for `ui_components`

Confirm that `ui_components.py` is in the same directory as `app.py`. Confirm that the file uses a supported Python version and that Streamlit is installed in the active environment.

### `ImportError` for `document_processor` or `rag_engine`

Confirm that both backend modules are committed to the repository and use the exact filenames imported by `app.py`.

### Documents upload but indexing fails

Inspect the backend parser dependencies and confirm that the uploaded file contains extractable text. Scanned PDFs may require OCR support. Spreadsheet and DOCX support must be implemented by `DocumentProcessor`.

### Chat memory does not survive deployment

This is usually caused by an ephemeral hosting filesystem. Use a persistent database instead of `chat_memory.json` when memory must survive redeployments or scale-out.

### Preview is empty

The preview displays extracted text from `DocumentProcessor.processed_docs`. If the parser returns no text, the preview cannot display content. Add OCR or a format-specific parser where required.

## Development checks

Run Python compilation checks before committing changes:

```bash
python -m py_compile app.py ui_components.py document_processor.py rag_engine.py
```

Run the Streamlit application locally:

```bash
streamlit run app.py
```

Test the complete path with a small representative document before deploying changes to production.

## License

Add the project’s license text here before publishing the repository. If no license is selected, the source code is not automatically available for unrestricted reuse.

## References

[1]: https://docs.streamlit.io/ "Streamlit Documentation"
[2]: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app "Streamlit Community Cloud Deployment Documentation"
[3]: https://docs.python.org/3/library/json.html "Python JSON Library Documentation"
[4]: https://docs.python.org/3/library/pathlib.html "Python pathlib Documentation"
