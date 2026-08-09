# 🏥 Medical Diagnosis Assistant

An AI-powered differential diagnosis tool built with Flask, LangChain, and advanced medical knowledge bases. This application provides healthcare professionals and medical students with intelligent symptom analysis and comprehensive differential diagnosis suggestions.

## ⚠️ Important Disclaimer

**This tool is for educational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical decisions.**

## 🚀 Features

### Core Functionality

-   **AI-Powered Analysis**: Advanced RAG (Retrieval-Augmented Generation) system using Groq LLM
-   **Comprehensive Medical Database**: Covers multiple disease categories including:
    -   🧠 Neurological conditions (Migraines, Headaches, Stroke)
    -   ❤️ Cardiovascular diseases (Hypertension, Myocardial Infarction)
    -   🫁 Respiratory disorders (Asthma, COPD, Pneumonia)
    -   🩺 Endocrine conditions (Diabetes Mellitus)
    -   🔬 And expanding medical knowledge base

### Technical Features

-   **Modern Web Interface**: Responsive Flask web application with Bootstrap 5
-   **Vector Database**: ChromaDB for efficient similarity search
-   **Real-time Analysis**: Fast symptom processing and differential diagnosis
-   **Educational Focus**: Detailed explanations and clinical reasoning

## 🛠️ Technology Stack

-   **Backend**: Python Flask
-   **AI Framework**: LangChain with Groq LLM
-   **Embeddings**: HuggingFace Transformers
-   **Vector DB**: ChromaDB
-   **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
-   **Icons**: Font Awesome

## 📋 Prerequisites

-   Python 3.8 or higher
-   Groq API key (free tier available)
-   HuggingFace token (optional, for embeddings)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ddx_project
```

### 2. Create Virtual Environment

```bash
python -m venv medical_assistant_env
source medical_assistant_env/bin/activate  # On Windows: medical_assistant_env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file and add your API keys:

```
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
SECRET_KEY=your-secret-key-for-production
```

### 5. Initialize the Medical Database

The application will automatically load and index medical documents on first run.

## 🚀 Running the Application

### Development Mode

```bash
python run_flask.py
```

### Production Mode

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app_flask:app
```

The application will be available at `http://localhost:5000`

## 📊 Medical Database

The system includes comprehensive clinical information for:

### Neurological Conditions

-   **Migraine**: Detailed pathophysiology, clinical presentation, and management
-   **Cluster Headache**: Diagnostic criteria and treatment approaches
-   **Tension Headache**: Clinical features and differential diagnosis
-   **Stroke**: Comprehensive cerebrovascular accident management

### Cardiovascular Diseases

-   **Hypertension**: Classification, risk factors, and management strategies
-   **Myocardial Infarction**: STEMI/NSTEMI diagnosis and acute management

### Respiratory Disorders

-   **Asthma**: Phenotypes, control assessment, and stepwise management
-   **COPD**: Staging, exacerbation management, and prevention
-   **Pneumonia**: Community and hospital-acquired types, treatment protocols

### Endocrine Conditions

-   **Diabetes Mellitus**: Type 1/2 classification, complications, management

## 🔍 How It Works

### 1. Symptom Input

Users provide detailed patient symptoms and clinical presentation through the web interface.

### 2. AI Processing

-   Symptoms are converted to embeddings using HuggingFace models
-   ChromaDB performs similarity search against medical knowledge base
-   Most relevant medical documents are retrieved

### 3. LLM Analysis

-   Groq LLM analyzes symptoms against retrieved medical context
-   Generates ranked differential diagnoses with clinical reasoning
-   Provides detailed explanations and recommendations

### 4. Results Display

-   Comprehensive analysis with differential diagnoses
-   Clinical reasoning and supporting evidence
-   Recommendations for further evaluation

## 🎯 Usage Examples

### Example 1: Cardiovascular Symptoms

**Input**: "45-year-old male presents with crushing chest pain, diaphoresis, and shortness of breath for 2 hours"

**AI Analysis**: Provides differential including myocardial infarction, unstable angina, with detailed reasoning.

### Example 2: Neurological Symptoms

**Input**: "Unilateral throbbing headache with photophobia and nausea lasting 6 hours"

**AI Analysis**: Analyzes migraine vs other headache types with clinical distinctions.

## 🔒 Security & Privacy

-   No patient data is stored permanently
-   API keys are securely managed through environment variables
-   All processing is done locally (except LLM API calls)
-   HTTPS recommended for production deployment

## 📱 Browser Compatibility

-   ✅ Chrome/Chromium 90+
-   ✅ Firefox 88+
-   ✅ Safari 14+
-   ✅ Edge 90+

## 🔧 Configuration

### Environment Variables

```
FLASK_APP=app_flask.py
FLASK_ENV=development
DEBUG=True
PORT=5000
GROQ_API_KEY=your_api_key
HF_TOKEN=your_token
SECRET_KEY=your_secret_key
```

### Medical Database Extension

To add new medical conditions:

1. Create `.txt` files in the `data/` directory
2. Follow the existing format with comprehensive clinical information
3. Restart the application to reindex the database

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app_flask:app"]
```

### Heroku Deployment

1. Create `Procfile`:

```
web: gunicorn app_flask:app
```

2. Set environment variables in Heroku dashboard
3. Deploy using Git or GitHub integration

## 🧪 Testing

Run basic functionality tests:

```bash
python -m pytest tests/  # If test suite is available
```

Manual testing checklist:

-   [ ] Application starts without errors
-   [ ] Medical database loads successfully
-   [ ] Symptom analysis returns results
-   [ ] All pages render correctly
-   [ ] Responsive design works on mobile

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/medical-condition`)
3. Add comprehensive medical documentation
4. Test thoroughly with medical professionals
5. Submit a pull request

### Medical Content Guidelines

-   Use evidence-based medical literature
-   Include diagnostic criteria, clinical presentation, and management
-   Cite relevant medical guidelines and research
-   Review with qualified medical professionals

## 📋 Roadmap

### Phase 1 (Current)

-   ✅ Core RAG implementation
-   ✅ Flask web interface
-   ✅ Basic medical database

### Phase 2 (Planned)

-   [ ] Advanced medical imaging integration
-   [ ] Multi-language support
-   [ ] Enhanced clinical decision support
-   [ ] Integration with medical databases (ICD-10, SNOMED)

### Phase 3 (Future)

-   [ ] Mobile application
-   [ ] Real-time collaboration features
-   [ ] Advanced analytics and reporting
-   [ ] Medical education modules

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For technical support or medical content questions:

-   Create an issue on GitHub
-   Contact the development team
-   Review documentation and FAQ

## 🙏 Acknowledgments

-   Medical professionals who provided clinical expertise
-   Open-source communities for frameworks and libraries
-   Educational institutions supporting medical AI research

---

**Remember**: This tool is designed to supplement, not replace, clinical judgment and professional medical consultation. Always prioritize patient safety and seek qualified medical advice for actual patient care.
