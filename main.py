import openai
import os
import logging


logging.basicConfig(level=logging.INFO)


def main():
    job_descriptions = [
        "job_descriptions/job_description_1.txt",
        "job_descriptions/job_description_2.txt",
    ]

    for jd_filepath in job_descriptions:
        with open(jd_filepath, "r") as infile:
            jd = infile.read()
        
        with open("resume.txt", "r") as infile:
            resume_contents = infile.read()

        PROMPT = PROMPT_TEMPLATE.format(resume=resume_contents, job_description=jd)
        text_response = prompt_gpt(PROMPT)
        output_filepath = jd_filepath.split("/")[1]
        save_coverletter(f"output_coverletter/{output_filepath}", text_response)


def prompt_gpt(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.6,
        max_tokens=1500
    )

    return response.choices[0].text


def save_coverletter(output_filepath, file_contents):
    with open(output_filepath, "w") as outfile:
        outfile.write(file_contents)


PROMPT_TEMPLATE = """
Write a cover letter for the following 

Resume
{resume}

and the following job description
{job_description}
"""

if __name__ == "__main__":
    logging.info("Starting script")
    main()
    logging.info("Finished script")
