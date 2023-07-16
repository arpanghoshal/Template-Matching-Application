import streamlit as st
import pandas as pd
from app_utils import generate_transformation_instructions, generate_correction_instructions, generate_transformation_code

# Set title of the web page
st.title('Template Matching Application')
# Set a markdown text and hyperlink to developer's LinkedIn profile
st.markdown('Made by [Arpan Ghoshal](https://www.linkedin.com/in/arpanghoshal/)')

# File uploaders for uploading template and user tables
template_file = st.file_uploader("Upload your Template Table", type=['csv'])
user_file = st.file_uploader("Upload your table to transform", type=['csv'])

# Get the OpenAI API Key from streamlit secrets
openai_api_key=st.secrets['openai']['OPENAI_API_KEY']



# If both files are uploaded
if user_file and template_file:
    # Generate transformation instructions
    json_output, error = generate_transformation_instructions(user_file, template_file, openai_api_key)
    if error is not None:
        # Display any errors
        st.write(f"An error occurred: {error}")
    else:
        # Show the generated JSON output
        st.json(json_output)
        # Allow user to confirm whether the JSON is correct
        is_correct = st.selectbox('Is the generated json correct?', ['Yes', 'No'])
        if is_correct == 'No':
            # If not, ask the user for correction details
            not_correct = st.text_input('Please indicate what is not correct:')
            st.caption('Example: new_Date_format should be MM-dd-yyyy')
            if not_correct:
                # Generate corrected transformation instructions
                json_output, error = generate_correction_instructions( json_output, not_correct, openai_api_key)
                if error is not None:
                    # Display any errors
                    st.write(f"An error occurred: {error}")
                else:
                    # Show the corrected JSON output
                    st.json(json_output)
                    # Allow user to generate corrected transformation code
                    if st.button('Generate Corrected Transformation Code'):
                        code_output, error = generate_transformation_code(  json_output, openai_api_key)
                        if error is not None:
                            # Display any errors
                            st.write(f"An error occurred: {error}")
                        else:
                            # Display the generated transformation code
                            st.code(code_output)
                            st.write("Please copy the code and run it in your local machine.")
        elif is_correct == 'Yes':
            # If the JSON is correct, allow user to generate transformation code
            if st.button('Generate Transformation Code'):
                code_output, error = generate_transformation_code(json_output, openai_api_key)
                if error is not None:
                    # Display any errors
                    st.write(f"An error occurred: {error}")
                else:
                    # Display the generated transformation code
                    st.code(code_output)
                    st.write("Please copy the code and run it in your local machine.")
                    st.caption('Refresh the page to try with another pair of files.')

    
else:
    # If both files are not uploaded, ask the user to upload both
    st.write("Please upload both files.")


