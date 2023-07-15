import streamlit as st
from langchain_helper import generate_transformation_instructions, generate_correction_instructions, generate_transformation_code

st.title('Template Matching Application')
st.markdown('Made by [Arpan Ghoshal](https://www.linkedin.com/in/arpanghoshal/)')

template_file = st.file_uploader("Upload your Template Table", type=['csv'])
user_file = st.file_uploader("Upload your table to transform", type=['csv'])

openai_api_key=st.secrets['openai']['OPENAI_API_KEY']

if user_file and template_file:
    json_output, error = generate_transformation_instructions(user_file, template_file, openai_api_key)
    if error is not None:
        st.write(f"An error occurred: {error}")
    else:
        st.json(json_output)
        is_correct = st.selectbox('Is the generated json correct?', ['Yes', 'No'])
        if is_correct == 'No':
            not_correct = st.text_input('Please indicate what is not correct:')
            if not_correct:
                json_output, error = generate_correction_instructions(json_output, not_correct, openai_api_key)
                if error is not None:
                    st.write(f"An error occurred: {error}")
                else:
                    st.json(json_output)
                    if st.button('Generate Corrected Transformation Code'):
                        code_output, error = generate_transformation_code(json_output, openai_api_key)
                        if error is not None:
                            st.write(f"An error occurred: {error}")
                        else:
                            st.code(code_output)
                            st.write("Please copy the code and run it in your local machine.")
        elif is_correct == 'Yes':
            if st.button('Generate Transformation Code'):
                code_output, error = generate_transformation_code(json_output, openai_api_key)
                if error is not None:
                    st.write(f"An error occurred: {error}")
                else:
                    st.code(code_output)
                    st.write("Please copy the code and run it in your local machine.")
else:
    st.write("Please upload both files.")
st.markdown('3 hours project using Langchain and OpenAI: [Project Link](https://github.com/arpanghoshal/Template-Matching-Application)')
