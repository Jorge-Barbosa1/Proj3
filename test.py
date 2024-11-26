#pip install langchain-ollama streamlit pymupdf streamlit-markdown
from langchain_ollama import OllamaLLM # Import the OllamaLLM class from langchain_ollama
import streamlit as st 
import fitz # PyMuPDF to extract text from PDF

#
llm= OllamaLLM(model="llama3") # Call the LLM model

#Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = "" # Initialize an empty string

    try:
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf:  
            for page in pdf:
                text += page.get_text() # Extract text from each page and append to the text variable
            return text
    except Exception as e:
        return f"Error processing the PDF file: {e}"
    
#Function to generate mindmap using 
def generate_mindmap(text):
    lines= text.split("\n") # Split the text into lines
    mindmap = "# Mindmap\n" # Initialize the mindmap with a heading
    for line in lines:
        if line.strip():
            mindmap += f"- {line.strip()}\n"  
    return mindmap


# Streamlit app
st.title("PDF Reader with LLama3")

promt = st.text_area("Enter your prompt here:") 

uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"]) # File uploader for PDF files

if uploaded_pdf:
    st.info("PDF file uploaded successfully!")
    
    #Extract text from the PDF file
    with st.spinner("Extracting text from PDF..."):
        extracted_text = extract_text_from_pdf(uploaded_pdf)
    
    #Display the extracted text
    st.subheader("Extracted text from the PDF file:")
    st.write(extracted_text)

if st.button("Submit"):
    if promt or uploaded_pdf:
        with st.spinner("Thinking..."):
            
            input_text = promt if promt else extracted_text
            final_prompt = (
                f"Escreve tópicos para fazer um mapa mental sobre o pdf:\n\n{input_text}"
            )
            try:
                # Call the model and display the output
                response = llm.invoke(final_prompt, stop=['<|eot_id|>'])
                st.subheader("Model response:")
                st.write(response)

                mindmap = generate_mindmap(response)
            
                # Save the mindmap to a file
                html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader"></script>
                    </head>
                    <body>
                        <svg id="markmap"></svg>
                        <script>
                            const markdown = `{mindmap}`;
                            const root = window.markmap.parse(markdown);
                            window.markmap.Markmap.create('#markmap', null, root);
                        </script>
                    </body>
                    </html>
                """

                st.subheader("Mindmap:")
                st.components.v1.html(html_content, height=600, scrolling=True)
            except Exception as e:
                st.error(f"Erro ao processar o modelo: {e}")

    else: 
        st.warning("Please enter a prompt or upload a PDF file")
            