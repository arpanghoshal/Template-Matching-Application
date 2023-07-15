# Template Matching Application

## Overview

The Template Matching Application is a tool that utilizes Langchain and OpenAI to transform a user's data to match a specific template. Users upload their data and a template file in CSV format, and the application generates instructions for transforming the data to match the template. These instructions are then converted into Python code, which the user can run on their local machine.

## File Structure

The project is structured as follows:

- `app.py`: This is the main application file. It contains the user interface logic and interacts with the helper functions defined in `app_utils.py`.
- `app_utils.py`: This file contains all the helper functions used in the application for loading CSV files, running the LLMChain, and generating transformation instructions, correction instructions, and transformation code.

## Function Descriptions

`app_utils.py` contains the following functions:

- `load_csv(file)`: This function takes a file path as an argument and uses pandas to load the CSV file. It returns a DataFrame containing the file data.

- `run_llm_chain(llm, prompt, variables)`: This function runs an LLMChain using the provided language model, prompt, and variables.

- `generate_transformation_instructions(user_file, template_file, openai_api_key)`: This function takes the user's file, the template file, and the OpenAI API key as arguments. It generates transformation instructions using the ChatOpenAI model and returns a JSON object detailing the instructions.

- `generate_correction_instructions(json_output, not_correct, openai_api_key)`: This function takes the original transformation instructions, user feedback, and the OpenAI API key as arguments. It generates corrected transformation instructions based on the user's feedback.

- `generate_transformation_code(json_output, openai_api_key)`: This function takes the transformation instructions and the OpenAI API key as arguments. It generates Python code for performing the data transformation based on the instructions.

## Usage

1. Clone this repository:

```bash
git clone https://github.com/arpanghoshal/Template-Matching-Application.git
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit application:

```bash
streamlit run app.py
```

4. Access the application in your browser via the localhost URL that Streamlit provides (usually `http://localhost:8501`).

5. Follow the prompts in the application to upload your data and template files, verify the generated transformation instructions, and generate your transformation code.

## Contributing

Contributions are welcome! Please fork this repository and create a Pull Request with your changes.

## License

This project is licensed under the terms of the MIT license.

## Author

[Arpan Ghoshal](https://www.linkedin.com/in/arpanghoshal/)


