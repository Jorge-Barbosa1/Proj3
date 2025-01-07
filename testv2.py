# pip install langchain-ollama streamlit pymupdf streamlit-markdown SpeechRecognition pydub
import streamlit as st
from langchain_ollama import OllamaLLM
import fitz # PyMuPDF to extract text from PDF
import speech_recognition as sr 
from pydub import AudioSegment # AudioSegment to convert audio file to wav format
from io import BytesIO
from graphviz import Digraph
import streamlit.components.v1 as components
import os 

#Constants
MODEL_NAME = "llama3" 
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

#Start the model
llm= OllamaLLM(model=MODEL_NAME,base_url=OLLAMA_URL)

#Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file"""
    try:
        text = ""
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error processing the PDF: {e}")
        return None
    
#Function to convert audio file to text
def convert_audio_to_text(audio_file):
    """Convert audio file to text"""
    recognizer = sr.Recognizer()
    try:
        #Convert audio file to .wav
        audio= AudioSegment.from_file(audio_file)
        audio_wav = BytesIO()
        audio.export(audio_wav, format="wav")
        audio_wav.seek(0)

        #Convert to text
        with sr.AudioFile(audio_wav) as source:
            audio_data = recognizer.record(source)
            return recognizer.recognize_google(audio_data)
    except Exception as e:
        st.warning(f"Error converting audio to text: {e}")
        return None
    except sr.UnknownValueError:
        #Error handling for "unreadable" audio
        st.warning("Audio file could not be understood") 
        return None    

# Function to generate mindmap structure
def generate_mindmap_structure(text):
    mindmap = {}
    lines = text.strip().split('\n')
    
    current_topic = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.endswith(':'):
            current_topic = line[:-1] 
            mindmap[current_topic] = []
        elif current_topic:
            mindmap[current_topic].append(line)
    
    return mindmap


# Function to render and display the mindmap
def render_mindmap_as_image(mindmap):
    try:
       
        dot = Digraph(comment="Mapa Mental")
        dot.attr(rankdir="LR") 

        # Adicione os nós e conexões ao grafo
        for topic, subtopics in mindmap.items():
            dot.node(topic, topic) 
            for subtopic in subtopics:
                dot.node(subtopic, subtopic) 
                dot.edge(topic, subtopic) 
        

        svg_code = dot.pipe(format="svg").decode("utf-8")

        
        components.html(svg_code, height=500, scrolling=True)
    except Exception as e:
        st.error(f"Erro ao renderizar o mapa mental: {e}")



#Main 
def main():
    st.title("PDF and Audio Reader with LLama3")

    st.subheader("Input")
    promt = st.text_area("Enter your prompt here:")
    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
    uploaded_audio = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

    #Process the PDF file
    pdf_text = None
    if uploaded_pdf:
        st.info("PDF file uploaded successfully!")
        with st.spinner("Extracting text from PDF..."):
            pdf_text = extract_text_from_pdf(uploaded_pdf)
        if pdf_text:
            st.subheader("Extracted text from the PDF file:")
            st.write(pdf_text)

    #Process the audio file
    audio_text = None
    if uploaded_audio:
        st.info("Audio file uploaded successfully!")
        with st.spinner("Converting audio to text..."):
            audio_text = convert_audio_to_text(uploaded_audio)
        if audio_text:
            st.subheader("Extracted text from the audio file:")
            st.write(audio_text)

    #Generate the mindmap structure
    if st.button("Submit"):
        input_text = promt or pdf_text or audio_text

        if not input_text:
            st.warning("Please provide a prompt or upload a PDF or audio file")
            return
        
        st.subheader("Thinking...")
        with st.spinner("Generating"):
            try:
                final_prompt = (
                    f"Escreve tópicos para fazer um mapa mental sobre o seguinte texto:\n\n{input_text}"
                    )
                response = llm.invoke(final_prompt, stop=['<|eot_id|>'])
                
                #Display the structured response
                st.subheader("Model response:")
                st.write(response)

                #Generate the mindmap
                mindmap = generate_mindmap_structure(response)
                st.subheader("Mindmap Structure:")
                st.write(mindmap)
                
                st.subheader("Mindmap:")
                render_mindmap_as_image(mindmap)
            
            except Exception as e:
                st.error(f"Error processing the model: {e}")

#Run the main function
if __name__ == "__main__":
    main()

    
