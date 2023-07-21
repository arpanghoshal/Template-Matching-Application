import streamlit as st
from app_utils import AppUtils

# Instantiate AppUtils object
app_utils = AppUtils()

st.title('Template Matching Application')
st.markdown('Made by [Arpan Ghoshal](https://www.linkedin.com/in/arpanghoshal/)')

st.markdown('Example Template File and File to Transform [Click Here](https://drive.google.com/file/d/1YldCXidwvwnqklun8xe6f7Xy3deESroJ/view?usp=sharing)')

template_file = st.file_uploader("Upload your Template Table", type=['csv'])
user_file = st.file_uploader("Upload your table to transform", type=['csv'])

openai_api_key=st.secrets['openai']['OPENAI_API_KEY']

if user_file and template_file:
    json_output, error = app_utils.generate_transformation_instructions(user_file, template_file, openai_api_key)
    if error is not None:
        st.write(f"An error occurred: {error}")
    else:
        st.json(json_output)
        is_correct = st.selectbox('Is the generated json correct?', ['Yes', 'No'])
        if is_correct == 'No':
            not_correct = st.text_input('Please indicate what is not correct:')
            st.caption('Example: new_Date_format should be MM-dd-yyyy')
            if not_correct:
                json_output, error = app_utils.generate_correction_instructions(json_output, not_correct, openai_api_key)
                if error is not None:
                    st.write(f"An error occurred: {error}")
                else:
                    st.json(json_output)
                    if st.button('Generate Corrected Transformation Code'):
                        code_output, error = app_utils.generate_transformation_code(json_output, openai_api_key)
                        if error is not None:
                            st.write(f"An error occurred: {error}")
                        else:
                            st.code(code_output)
                            st.write("Please copy the code and run it in your local machine.")
        elif is_correct == 'Yes':
            if st.button('Generate Transformation Code'):
                code_output, error = app_utils.generate_transformation_code(json_output, openai_api_key)
                if error is not None:
                    st.write(f"An error occurred: {error}")
                else:
                    st.code(code_output)
                    st.write("Please copy the code and run it in your local machine.")
                    st.caption('Refresh the page to try with another pair of files.')
else:
    st.write("Please upload both files.")
