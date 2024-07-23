# Job Search and CV Generation with CrewAI

## Overview
Welcome to **Job Search and CV Generation with CrewAI**.
This project uses CrewAI and Gemini to automize job searching and generate your CV and cover letter based on your experience and jobs requirements.

## Features
* Multi-agent crew to analyze your CV, look for jobs based on your experience and desired job, and generate a tailored CV and cover letter for each job opportunity.
* Integration with Google's Gemini and other LLMs to power the agents and generate your CV and cover letter.

## Getting Started
### Prerequisites
Before you begin, ensure you have the following:
* Python 3.12
* CrewAI 0.32
* Langchain 0.1.20
* Langchain Google GenAI 1.0.6
* Access to Gemini or another LLM API
* [Serper.dev](https://serper.dev/) API key
* Environment variables set up for your API credentials

### Installation

#### 1. Clone the repository
```sh
git clone https://github.com/Malegiraldo22/JobSearch
cd JobSearch
```

#### 2. Install dependencies
```sh
pip install -r requirements.txt
```

#### 3. Set up environment variables
Create a `.env` file in the project directory with the following content:
```
GEMINI_KEY = your_gemini_key
SERPER_API_KEY = your_serper_api_key
```

### Usage
Run the app:
```sh
python main.py
```

## Detailed Description

### Agents
The `agents.py` file contains the agents needed to run the crew:
#### CV Analyst
Makes a short resume of your CV and extracts information from it.
#### Job Search Analyst
Searches for jobs based on your CV, experience and desired jobs opportunities.
#### CV Writer
Uses the jobs found and your resume to write a CV and cover letter tailored for each job found.
#### Career Coach
Evaluates the new CV and cover letter, providing recommendations and orientation on how to prepare for a possible interview.

### Tools
The agents use tools to find job opportunities from either Google Jobs or job posting websites or to make searches to improve your CV.

#### Search on google jobs
This tool is used to find jobs and scrape its content from Google jobs.

#### Search on internet
This tool is used by the crew to search the internet about a given topic and return relevant results. It uses the Serper.dev API to make the search, returning a list of the top 5 results with the title, link, date if available, and a snippet.

#### Scrape data from website
This tool uses CrewAI ScrapeWebsiteTool to scrape data from a website.

#### Save markdown
Saves the final output in a markdown file.

### Tasks
The agents follow the next tasks to do their jobs:

#### Analyze CV
Analyzes your CV and extracts:
- Experience
- Skills
- Career fields
- Possible types of companies that you might be interested to work

#### Find Jobs
Searches for job opportunities based on your job preference, location and CV. It returns:
- Company name
- Job position
- Salary
- Location
- Job ofer abstract
- Link

**Note**: The search is limited to two job opportunities due to potential context loss with more results. This might be due to Gemini's token limits on their free tier. It might work better with ChatGPT-4 as CrewAI is highly dependent on it.

#### Create custom resume and cover letter
Uses the jobs found to tailor a CV and cover letter based on your original CV and the requirements for each job position.

#### Provide job search guidance and interview prep
Uses each job posting and generated CV to provide guidance on how to prepare for a possible job interview. It also saves the final output in a markdown file.

### Main
The main script `main.py` orchestrates the agents and overall workflow. It's possible to change the LLM model used to handle the crew in this file.

#### LLM model configuration
Depending on the model you'll need to import a different library to handle your LLM model check more [here](https://docs.crewai.com/how-to/LLM-Connections/)

## Limitations
* Gemini's token and RPM limits on their free tier can cause the crew to take a lot of time to finish the tasks, sometimes leading to context loss and generating fake job opportunities and CVs.
* Working with ChatGPT is possible and recommended as CrewAI is designed to use it as its main LLM source.
* Working with local LLMs like Llama 3, Mistral, or Gemma is possible using either Ollama or Groq, but CrewAI tends to have difficulty working with local LLMs.

## Contributing
Contributions are welcome! Please fork this repository and submit a pull request with your changes.

## Contact
For any questions or comments, please open an issue on GitHub or contact me directly at magiraldo2224@gmail.com