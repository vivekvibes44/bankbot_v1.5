# 🏦 BankBot v1.5 — Agentic AI Banking Assistant

An Agentic AI-powered banking assistant built with **Python, Streamlit, LangGraph, Groq, OpenRouter, FAISS, and SQLite**.

BankBot v1.5 transforms a conventional banking RAG chatbot into a tool-using AI assistant capable of answering banking questions, performing loan calculations, analyzing simulated transactions, and managing customer complaints through human-approved workflows.

> **Note:** Ready Bank is a fictional banking institution. This project is developed for educational and portfolio purposes. It does not connect to real banking systems or perform actual financial transactions.

---

## 📌 Project Overview

Traditional RAG chatbots primarily retrieve information from documents and generate responses based on the retrieved content.

BankBot v1.5 extends this approach by introducing an agentic architecture using **LangGraph**.

The agent can interpret user requests, select relevant tools, execute banking operations, and present structured results through an interactive Streamlit interface.

The application combines:

- Retrieval-Augmented Generation (RAG) for banking knowledge.
- LLM-based tool selection and execution.
- Deterministic Python banking tools.
- SQLite-based simulated banking data.
- Human-in-the-loop complaint approval.
- Conversation state and agent activity tracking.

## ✨ Features

### 🤖 AI Banking Assistant
- Natural-language banking conversations.
- LangGraph-based single-agent orchestration.
- LLM tool selection and execution.
- Conversational context using thread-based state management.
- Structured result presentation.
- Agent activity and tool execution history.

### 📚 Retrieval-Augmented Generation
- Ready Bank knowledge base.
- Document loading and text chunking.
- OpenRouter-hosted embedding models.
- FAISS vector similarity search.
- Banking knowledge retrieval through an agent tool.
- Source information displayed in assistant responses.

### 💰 Loan Assistance
- EMI calculation.
- Total interest and repayment calculation.
- Preliminary loan eligibility assessment.
- Loan product comparison.
- Structured calculation results.

### 📊 Transaction Analysis
- Synthetic customer and account records.
- Transaction history.
- Spending summaries.
- Category-wise spending analysis.
- Monthly spending analysis.

### 🎧 Complaint Management
- Simulated complaint registration.
- Complaint category and description validation.
- Unique complaint reference generation.
- Complaint tracking.
- Human approval and rejection using LangGraph interrupts.

### 🖥️ Interactive Banking Dashboard
- Modular Streamlit interface.
- Seven application pages.
- Dashboard metrics.
- Light and Dark themes.
- Quick navigation and banking shortcuts.
- Agent execution visibility.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| LLM Provider | Groq |
| Agent Orchestration | LangGraph |
| LLM Integration | LangChain |
| Embedding Provider | OpenRouter |
| Vector Search | FAISS |
| Document Processing | PyPDF |
| Text Splitting | LangChain Text Splitters |
| Database | SQLite |
| Configuration | Python dotenv |

---

## 🏗️ Architecture Overview

BankBot v1.5 follows a modular architecture with separate presentation, agent, tool, knowledge, and data layers.

text
                  USER
                    |
                    v
          STREAMLIT APPLICATION
                    |
          +---------+----------+
          |         |          |
          v         v          v
       Dashboard  Assistant   Other Pages
                    |
                    v
             LANGGRAPH AGENT
                    |
              GROQ LLM
                    |
             TOOL SELECTION
                    |
        +-----------+------------+
        |           |            |
        v           v            v
    Loan Tools  Complaint    Transaction
                Tools          Tools
        |           |            |
        |           v            |
        |      Human Approval    |
        |           |            |
        +-----------+------------+
                    |
                    v
              SQLITE DATABASE


          BANKING KNOWLEDGE RETRIEVAL
                    |
             Knowledge Documents
                    |
                    v
             Document Loading
                    |
                    v
              Text Splitting
                    |
                    v
           OPENROUTER EMBEDDINGS
                    |
                    v
              FAISS INDEX
                    |
                    v
             KNOWLEDGE TOOL
                    |
                    v
               LANGGRAPH


### Core Components

**1. Presentation Layer**

Streamlit provides the interactive banking interface through modular pages.

**2. Agent Layer**

LangGraph manages the agent workflow, tool execution, conversation state, and human approval interrupts.

**3. Tool Layer**

Specialized Python tools handle loan calculations, eligibility checks, complaint operations, transaction analysis, and banking knowledge retrieval.

**4. Knowledge Layer**

The RAG pipeline loads banking documents, splits them into chunks, generates embeddings, and retrieves relevant information using FAISS.

**5. Data Layer**

SQLite stores simulated customers, accounts, transactions, and complaints.

---

## 📂 Project Structure

text
Bankbot_v1_5/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
│
├── agents/
│   └── graph.py
│
├── database/
│   ├── db.py
│   ├── complaint_repository.py
│   └── transaction_repository.py
│
├── tools/
│   ├── complaint_tools.py
│   ├── loan_tools.py
│   ├── transaction_tools.py
│   └── knowledge_tool.py
│
├── rag/
│   └── ...
│
├── ui/
│   ├── common.py
│   ├── dashboard.py
│   ├── assistant.py
│   ├── loans.py
│   ├── transactions.py
│   ├── support.py
│   ├── activity.py
│   └── settings.py
│
├── tests/
│   └── ...
│
├── knowledge/
│   └── ...
│
└── vector_store/
    └── faiss_index/


*The directory listing highlights the main application modules. Additional files may exist within individual directories.*

---

## ⚙️ Installation and Setup

### 1. Clone the Repository


git clone https://github.com/vivekvibes44/bankbot_v1.5
cd Bankbot_v1_5


Replace the placeholder with your actual GitHub repository URL.

### 2. Create a Virtual Environment


python -m venv .venv


Activate it on Windows:

powershell
.venv\Scripts\activate


### 3. Install Dependencies


pip install -r requirements.txt


### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Add the following configuration variables:

env
# Groq Configuration
GROQ_API_KEY=your_groq_api_key
GROQ_BASE_URL=your_groq_base_url
LLM_MODEL=your_groq_model

# OpenRouter Configuration
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=your_openrouter_base_url
EMBEDDING_MODEL=your_embedding_model
TEST_EMBEDDING_MODEL=your_test_embedding_model


Obtain the required API credentials from:

- Groq: https://console.groq.com/
- OpenRouter: https://openrouter.ai/

**Important:** Never commit your `.env` file or expose API credentials in your GitHub repository.

### 5. Run the Application

From the project root directory:


streamlit run app.py


Streamlit will start the application and provide a local URL, typically:

text
http://localhost:8501


---

## 🚀 Application Modules

| Page | Description |
|---|---|
| Dashboard | Overview metrics and quick navigation |
| AI Assistant | Banking conversations, RAG, and agent execution |
| Loans | EMI calculator, loan comparison, and eligibility |
| Transactions | Transaction history and spending analysis |
| Support | Complaint registration and tracking |
| Activity | Agent tool execution history |
| Settings | Application theme information |

---

## 🔄 Example Use Cases

The following example prompts demonstrate the application's capabilities.

**Banking Knowledge**
- What is the minimum balance required for a Ready Bank savings account?
- What is the replacement debit card fee?

**Loan Assistance**
- Calculate EMI for a loan of ₹500,000 at 10% interest for 60 months.
- Compare the available loan products.
- Check eligibility for a personal loan.

**Transaction Analysis**
- Show transactions for account RB-ACC-1002.
- Give me a spending summary for this account.
- Show my category-wise spending.
- Provide monthly spending analysis.

**Complaint Management**
- I want to register a complaint about my debit card.
- Track my complaint using its reference number.

Complaint registration requires explicit approval before the simulated ticket is created.

---

## 🔐 Safety and Data Boundaries

- Ready Bank is fictional.
- Customer, account, and transaction records are synthetic.
- The application does not connect to real bank accounts.
- No actual financial transactions are performed.
- Loan eligibility results are estimates, not official approvals.
- Complaint registration requires user confirmation.
- API credentials must be stored in environment variables.

---

## 🧪 Testing

The project includes tests for individual tools and core application functionality.

Tested areas include:

- EMI calculation accuracy.
- Loan eligibility validation.
- Loan product comparison.
- Complaint input validation.
- Complaint approval and cancellation.
- Complaint tracking.
- Customer and account verification.
- Transaction retrieval.
- Spending calculations.
- RAG retrieval.
- Agent tool integration.

Run individual tests from the project root using Python module execution where applicable.

For example:


python -m tests.test_complaint_tools


Use the actual test module names present in the repository.

---

## 🎯 Project Objectives and Learning Outcomes

This project demonstrates practical implementation of:

- Agentic AI application development.
- LangGraph agent orchestration.
- LLM-based tool calling.
- Retrieval-Augmented Generation.
- Vector embeddings and FAISS similarity search.
- Deterministic Python tool development.
- SQLite database integration.
- Human-in-the-loop approval workflows.
- Modular Streamlit application development.
- Structured agent results and execution tracking.

---

## 🔮 Future Enhancements

Potential extensions, not included in the current implementation, include:

- Hybrid retrieval using semantic search and BM25.
- Advanced retrieval evaluation and reranking.
- Automated recurring transaction identification.
- Spending anomaly detection.
- Additional loan assistance workflows.
- More comprehensive workflow analytics.
- Deployment and production-readiness improvements.

---

## ⚠️ Disclaimer

BankBot v1.5 is an educational and portfolio-oriented software project.

It is not affiliated with any real banking institution. Ready Bank, its policies, customers, accounts, and transactions are fictional or simulated.

The application must not be used for real financial decisions, banking operations, or customer-data processing.

---

## 👨‍💻 Project

**BankBot v1.5 — Agentic AI Banking Assistant**

Built to demonstrate how Retrieval-Augmented Generation, LLM tool calling, LangGraph orchestration, deterministic Python tools, and human-in-the-loop workflows can work together in a practical banking application.

**Technologies:** Python · Streamlit · LangChain · LangGraph · Groq · OpenRouter · FAISS · SQLite