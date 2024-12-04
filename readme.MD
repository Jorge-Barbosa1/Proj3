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
  docker-compose up --build

---

Nota: Se der o erro de nao encontrar o modelo "llama3" abrir a cmd do docker "docker exec -it llama3_pdf-olama-1 bash" e  instalar llama3 "ollama pull llama3"

