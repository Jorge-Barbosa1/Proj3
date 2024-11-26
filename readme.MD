# 🦙 Llama3 PDF & Audio Processor

Este projeto é uma aplicação baseada no Streamlit que permite carregar arquivos PDF e MP3, extrair texto deles, e gerar mapas mentais usando um modelo LLM (Large Language Model) chamado **Llama3**.

## 🚀 Funcionalidades

- **Upload de arquivos PDF e MP3**
  - Extração de texto de arquivos PDF.
  - Transcrição de áudio (MP3) para texto usando a biblioteca `SpeechRecognition`.
  
- **Geração de Mapas Mentais**
  - Usa os tópicos gerados pelo LLM para criar mapas mentais renderizados com **Markmap**.

- **Interface Gráfica com Streamlit**
  - Fácil de usar, com suporte para upload de arquivos e prompts personalizados.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12**
- [Streamlit](https://streamlit.io) - Interface web.
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) - Extração de texto de PDFs.
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) - Transcrição de áudio.
- [Pydub](https://pypi.org/project/pydub/) - Processamento de áudio.
- **LangChain-Ollama** - Integração com LLMs.

---

## 📦 Como Configurar o Projeto

- **Docker** (opcional, mas recomendado para ambiente isolado).

```bash
  docker build -t projeto .
  docker run -p 8501:8501 projeto

---


### 2. Rodando Localmente (Sem Docker)

#### Passo 1: Clone o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
