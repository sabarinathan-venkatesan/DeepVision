import streamlit as st
from PIL import Image
import google.generativeai as genai
import pandas as pd
import io

# Set up the app title
st.title("Image-to-Text App with Gemini API")
st.write("Upload an image, enter a custom prompt, and the app will generate a textual description using Gemini.")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Custom prompt input
custom_prompt = st.text_input("Enter a custom prompt for the image:", "Describe the image in detail.")

# Configure Gemini API
genai.configure(api_key="ENTER YOUR API HERE")  # Replace with your Gemini API key

# Initialize the Gemini model
# Use 'gemini-1.5-flash' or 'gemini-1.5-pro' as the model name
model = genai.GenerativeModel('gemini-1.5-flash')  # or 'gemini-1.5-pro'

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Generate description using Gemini
    with st.spinner("Generating description..."):
        try:
            response = model.generate_content([custom_prompt, image])
            description = response.text
        except Exception as e:
            st.error(f"An error occurred: {e}")
            description = None

    # Display the generated description
    if description:
        st.write("Generated Description:")
        st.success(description)

        # Prepare data for CSV download
        data = {
            "Prompt": [custom_prompt],
            "Description": [description]
        }
        df = pd.DataFrame(data)

        # Convert DataFrame to CSV
        csv = df.to_csv(index=False).encode('utf-8')

        # Download button for CSV
        st.download_button(
            label="Download Description as CSV",
            data=csv,
            file_name="image_description.csv",
            mime="text/csv"
        )
