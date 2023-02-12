import openai
from dotenv import dotenv_values
import os

ENV_CONFIG = dotenv_values()
import logging

logging.basicConfig(level=logging.INFO)

PROMPT_TEMPLATE = """
Write a cover letter in markdown for the following 

Resume
{resume}

and the following job description
{job_description}


make sure you include a header that looks like the example below

Elizabeth Castillo
2987 W. Taylor Dr.
Portland, OR 45720
890-372-1262
cmleroix@anywhere.com

February 2, 2005

Amy Kincaid, Human Resource Director
Western Electric, Inc.
387 Collier Lane
Atlanta, Georgia 30051
"""


def main():
    with open("resume.txt", "r") as infile:
        resume_contents = infile.read()

    for jd_filename, jd_contents in generate_job_descriptions():
        logging.info(f"Processing '{jd_filename}'")
        PROMPT = PROMPT_TEMPLATE.format(
            resume=resume_contents, job_description=jd_contents
        )
        gpt_response = prompt_gpt(PROMPT)
        output_filepath = f"output_coverletter/{jd_filename}"
        save_coverletter(output_filepath, gpt_response)
        logging.info(f"Wrote '{output_filepath}'")


def prompt_gpt(prompt):
    openai.api_key = ENV_CONFIG["OPENAI_API_KEY"]
    response = openai.Completion.create(
        model="text-davinci-003", prompt=prompt, temperature=0.6, max_tokens=1500
    )

    return response.choices[0].text


def save_coverletter(output_filepath, file_contents):
    with open(output_filepath, "w") as outfile:
        outfile.write(file_contents)


import pathlib


def generate_job_descriptions(
    input_jd_path="job_descriptions", output_coverletter_path="output_coverletter"
):
    jd_glob = pathlib.Path(input_jd_path).glob("**/*")
    cl_glob = pathlib.Path(output_coverletter_path).glob("**/*")
    jd_files = set([x.name for x in jd_glob if x.is_file()])
    cl_files = set([x.name for x in cl_glob if x.is_file()])
    missing_files = jd_files - cl_files
    for filename in missing_files:
        target_filepath = pathlib.Path(input_jd_path) / pathlib.Path(filename)
        yield get_jd_meta(target_filepath)


def get_jd_meta(filepath):
    with open(filepath) as infile:
        jd_contents = infile.read()

    return filepath.name, jd_contents



if __name__ == "__main__":
    logging.info("Starting script")
    main()
    logging.info("Finished script")
