# pip install langchain-ollama streamlit pymupdf streamlit-markdown SpeechRecognition pydub
import streamlit as st
from langchain_ollama import OllamaLLM
import fitz # PyMuPDF to extract text from PDF
import speech_recognition as sr 
from pydub import AudioSegment # AudioSegment to convert audio file to wav format
from io import BytesIO

#Constants
MODEL_NAME = "llama3" 

#Start the model
llm= OllamaLLM(model=MODEL_NAME)

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

#Function to generate mindmap
def generate_mindmap(text):
    """Generate a mindmap from the text"""
    if not text :
        return None
    lines= text.split("\n")
    mindmap = "# Mindmap\n"
    for line in lines:
        if line.strip():
            mindmap += f"- {line.strip()}\n"
    return mindmap

#Function to display the mindmap
def display_mindmap(mindmap):
    """Display the mindmap on the Streamlit app"""
    if not mindmap:
        st.warning("Mindmap could not be generated")
        return
    
    #Display the mindmap using the streamlit markdown component
    markmap_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib/dist/index.umd.js"></script>
    </head>
    <body>
        <svg id="mindmap" style="width: 100%; height: 600px;"></svg>
        <script>
            const data = `{mindmap}`;
            const markmap = markmap.Markmap.create("#mindmap");
            markmap.setMarkdown(data);
        </script>
    </body>
    </html>
    """
    st.components.v1.html(markmap_template, height=650)

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
        with st.spinner("Generationg"):
            try:
                final_prompt = (
                    f"Escreve tópicos para fazer um mapa mental sobre o seguinte texto:\n\n{input_text}"
                    )
                response = llm.invoke(final_prompt, stop=['<|eot_id|>'])
                
                #Display the structured response
                st.subheader("Model response:")
                st.write(response)

                #Generate the mindmap
                mindmap = generate_mindmap(response)
                st.subheader("Mindmap:")
                display_mindmap(mindmap)
            
            except Exception as e:
                st.error(f"Error processing the model: {e}")

#Run the main function
if __name__ == "__main__":
    main()

    
