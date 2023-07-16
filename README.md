# Template Matching Application

## Overview

The Template Matching Application is a powerful tool that leverages Langchain and OpenAI to adapt user's data to align with a specific template. The application requires users to upload their data and a template file in CSV format. Subsequently, it formulates instructions for data transformation to match the template. These instructions are translated into Python code, which the user can execute on their local machine.

## Project Structure

The application is divided into two primary scripts:

- `app.py`: The primary application script that handles the user interface logic and interacts with the helper functions specified in `app_utils.py`.
- `app_utils.py`: This script encompasses all the helper functions leveraged in the application. These include functionalities for loading CSV files, running the LLMChain, and generating transformation instructions, correction instructions, and transformation code.

## Function Descriptions

`app_utils.py` comprises the following functions:

- `load_csv(file)`: Loads a CSV file using pandas given a file path and returns a DataFrame containing the file data.
- `run_llm_chain(llm, prompt, variables)`: Executes an LLMChain with the provided language model, prompt, and variables.
- `generate_transformation_instructions(user_file, template_file, openai_api_key)`: Generates transformation instructions using the ChatOpenAI model given the user's file, the template file, and the OpenAI API key, returning a JSON object containing the instructions.
- `generate_correction_instructions(json_output, not_correct, openai_api_key)`: Generates corrected transformation instructions based on the user's feedback, given the original transformation instructions and the OpenAI API key.
- `generate_transformation_code(json_output, openai_api_key)`: Generates Python code for data transformation based on the transformation instructions and the OpenAI API key.

## Usage Instructions

1. Clone this repository using the following command:

```bash
git clone https://github.com/arpanghoshal/Template-Matching-Application.git
```

2. Install the necessary packages using:

```bash
pip install -r requirements.txt
```

3. Start the Streamlit application with:

```bash
streamlit run app.py
```

4. Open the application in your browser using the localhost URL provided by Streamlit (typically `http://localhost:8501`).

5. Follow the application's prompts to upload your data and template files, validate the generated transformation instructions, and create your transformation code.

---

## Proposed Solution for Column Mapping Misalignment and Ambiguity in Assignments

**Project Demo:** [Link](https://template-matching-application.streamlit.app/)

**Algorithm for the Approach:** [Link](https://github.com/arpanghoshal/Template-Matching-Application/blob/main/psudo_algorithm_remove_misalign.py)

1. **Column Mapping:**

- Load user and template data.
- Generate 'user_embeddings' by encoding the first few rows of each user data column using a Language Model (like BERT).
- Produce 'template_embeddings' for each template data column.
- Compute the cosine similarity between 'user_embeddings' and 'template_embeddings' for each user-template column pair.
- Map each user column to the template column with the highest cosine similarity.

2. **Addressing Mapping Ambiguities:**

- Identify mappings where multiple user columns map to a single template column or vice versa.
- For each ambiguous mapping, provide the user with potential matches to confirm or choose the most appropriate match.

3. **Generating Transformation Logic:**

- Use GPT-3.5 to generate transformation logic for each mapped column pair, based on examples of the transformation process.

4. **Improving Accuracy Through Retraining:**

- **Approach 1 - Few-shot Learning:** Store the transformation logic as part of 'prompt_examples' for future transformations.
- **Approach 2 - Retraining the Model:** Continuously gather 'labeled_data' from each successful transformation. When enough 'labeled_data' has been accumulated, retrain the GPT model. [Link to the Algorithm Approach](https://github.com/arpanghoshal/Template-Matching-Application/blob/main/pseudo_algorithm_training.py)

5. **Post-Transformation Validation:**

- Apply the transformation logic to the user data to generate 'transformed_data.'
- Compare 'transformed_data' with the template format and notify the user of any inconsistencies.

---

## Contribution

We welcome contributions! Please fork this repository and introduce your changes through a Pull Request.

## License

This project operates under the terms of the MIT license.

## Author

[Arpan Ghoshal](https://www.linkedin.com/in/arpanghoshal/)

## Acknowledgement

This project was completed successfully within a mere 4-hour span, thanks to the efficiency and power of the Langchain and OpenAI libraries. The application underwent numerous rounds of iterative testing with varied prompting techniques to ensure accurate and robust outputs (transformation instructions and Python code). Designed to be user-friendly, the application offers an intuitive interface with interactive options for data upload, generation of transformation instructions, correction facilitation, and transformation code generation. It serves as an excellent illustration of the practical applications of language models.
