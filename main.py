from crewai import Crew, Process
import os
from textwrap import dedent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from agents import JobSearchAgents
from tasks import JobSearchTasks
from Tools.file_io import save_markdown

from dotenv import load_dotenv
load_dotenv()

class JobSearchCrew:
    def __init__(self, perfil, preferencias_trabajo, ubicacion):
        self.perfil = perfil
        self.preferencias_trabajo = preferencias_trabajo
        self.ubicacion = ubicacion
        self.Gemini = ChatGoogleGenerativeAI(model='gemini-1.5-pro',
                                             verbose=True,
                                             google_api_key=os.environ['GEMINI_KEY'])
        
        self.Llama = ChatGroq(model='gemma2-9b-it',
                              api_key = os.environ['GROQ_KEY'])

    def run(self):
        #Definir agentes y tareas en agents.py y tasks.py
        agents = JobSearchAgents()
        tasks = JobSearchTasks()

        #Definir agentes
        career_coach = agents.career_coach()
        cv_analyst = agents.cv_analyst()
        job_search_analyst = agents.job_search_analyst()
        cv_writer = agents.cv_writer()

        #Definir tareas
        analyze_cv = tasks.analyze_cv(
            cv_analyst,
            self.preferencias_trabajo,
            self.perfil,
            self.ubicacion
        )

        find_jobs = tasks.find_jobs(
            job_search_analyst,
            self.perfil,
            self.preferencias_trabajo,
            self.ubicacion,
            [analyze_cv]
        )

        cv_and_cover_letter_generation = tasks.create_custom_resume_and_cover_letter(
            cv_writer,
            self.perfil,
            [find_jobs],
            save_markdown
        )

        job_search_guidance_and_interview_prep = tasks.provide_job_search_guidance_and_interview_prep(
            career_coach,
            [cv_and_cover_letter_generation],
            save_markdown
        )

        compilador_archivo = tasks.compilador_archivo(
            career_coach,
            [job_search_guidance_and_interview_prep],
            save_markdown
        )

        crew = Crew(
            agents=[
                career_coach,
                cv_analyst,
                job_search_analyst,
                cv_writer
                ],
            tasks=[
                analyze_cv,
                find_jobs,
                cv_and_cover_letter_generation,
                job_search_guidance_and_interview_prep,
                compilador_archivo
                ],
            process = Process.hierarchical,
            manager_llm= self.Gemini,
            verbose=1
        )

        result = crew.kickoff()
        return result

#Main
if __name__ == "__main__":
    print("## Bienvenido a la busqueda de trabajo ##")
    print("-"*20)
    perfil = input(
        dedent("""
            Ingresa tu cv: 
            """)
    )

    preferencias_trabajo = input(
        dedent("""
            Qué posición laboral estás buscando?: 
            """)
    )

    ubicacion = input(
        dedent("""
            En qué ciudad quieres trabajar?
            """)
    )

    job_crew = JobSearchCrew(perfil, preferencias_trabajo, ubicacion)
    result = job_crew.run()
    print("-"*20)
    print("\n")
    print("Estas son las posiciones encontradas:\n")
    print(result)