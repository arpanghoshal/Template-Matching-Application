# Template Matching Application

## Description

The Template Matching Application is a web-based program designed to match user-specified tables (in CSV format) to a provided template table. It is mainly built using Python, Streamlit for web UI, and OpenAI's GPT-3.5-Turbo model along with Langchain for generating transformation instructions and code.

## How it works

The application uses two CSV files uploaded by the user: a user table and a template table. It then uses OpenAI's GPT-3 model to generate a JSON object detailing how to transform the user table to match the template table. The generated transformation instructions include details on column renaming, data transformations, and which columns to remove or keep.

If the user is not satisfied with the generated transformation, they can indicate the issues and the system will use the GPT-3 model again to generate corrected transformation instructions.

Finally, the system generates Python code, using pandas, based on the final transformation instructions. The user can then use this code to apply the transformations on their local machine.

## Dependencies

To use this application, you must have the following libraries installed:

- pandas
- langchain
- streamlit
- OpenAI's GPT-3 model (model='gpt-3.5-turbo')

## Usage

1. Start the application.
2. Upload your user table and template table (in CSV format).
3. The system will generate a JSON object detailing the transformation instructions. Review these instructions.
4. If the instructions are incorrect, provide details about the inaccuracies. The system will then generate corrected instructions.
5. After approving the transformation instructions, click the "Generate Transformation Code" button. The system will then generate Python code, which you can use to transform your user table on your local machine.

## Functions

`load_csv(file: object) -> pandas.DataFrame`  
Loads a CSV file into a pandas DataFrame. If an error occurs during loading, it is caught and displayed in the UI. Returns a DataFrame with the first 5 rows of the CSV file or None if an error occurs.

`run_llm_chain(llm: LLMChain, prompt: PromptTemplate, variables: dict) -> dict`  
Runs an instance of the LLMChain with the specified language model, prompt, and variables. If an error occurs during execution, it is caught and displayed in the UI. Returns the output of the LLMChain or None if an error occurs.

`generate_transformation_instructions(user_file: object, template_file: object) -> dict`  
Generates transformation instructions for converting a user table to match a template table. Returns a JSON object detailing the transformation instructions or None if an error occurs.

`generate_correction_instructions(json_output: dict, not_correct: str) -> dict`  
Generates corrected transformation instructions based on user feedback. Returns a JSON object detailing the corrected transformation instructions or None if an error occurs.

`generate_transformation_code(json_output: dict)`  
Generates Python code for applying transformations to the user table based on the transformation instructions. Displays the code in the UI.

## Authors

The Template Matching Application was created by Arpan Ghoshal as a 3-hour project. Try the app [here](https://template-matching-application.streamlit.app/).
