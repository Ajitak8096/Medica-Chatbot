import os
import gradio as gr
from brain_of_the_doctor import analyze_image_with_query, encode_image
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_voice_with_elevenlabs

# System prompt for the doctor AI
system_prompt = """You are a professional doctor analyzing a medical case. 
Please examine the information provided and give a concise medical opinion in 1-2 sentences.
Speak directly to the patient as if this were a real consultation."""

def process_inputs(audio_filepath, image_filepath):
    try:
        # Step 1: Transcribe audio
        speech_to_text = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
        
        if not speech_to_text:
            return "Could not transcribe audio", "", None

        # Step 2: Process image if provided
        encoded_image = encode_image(image_filepath) if image_filepath else None
        
        # Step 3: Generate doctor's response
        full_query = f"{system_prompt}\nPatient says: {speech_to_text}"
        doctor_response = analyze_image_with_query(
            query=full_query,
            encoded_image=encoded_image,
            model="llama3-70b-8192"
        )
        
        # Step 4: Generate voice response
        voice_response = text_to_voice_with_elevenlabs(
            input_text=doctor_response,
            output_filepath="doctor_response.mp3"
        )
        
        return speech_to_text, doctor_response, voice_response
        
    except Exception as e:
        return f"Error: {str(e)}", "", None

# Create Gradio interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Patient's Speech"),
        gr.Textbox(label="Doctor's Diagnosis"),
        gr.Audio(label="Voice Response")
    ],
    title="AI Medical Consultant",
    description="Speak your symptoms and optionally upload an image for analysis"
)

if __name__ == "__main__":
    iface.launch(debug=True)