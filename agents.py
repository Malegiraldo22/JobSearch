from crewai import Agent
from textwrap import dedent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from Tools.search_tool import SearchTool
import os
from dotenv import load_dotenv
load_dotenv()

class JobSearchAgents():
    #!: Gemini tiene un limite de 2RPM, evaluar si es necesario implementar el límite para cada agente
    def __init__(self):
        self.Gemini = ChatGoogleGenerativeAI(model='gemini-1.5-pro',
                                             verbose=True,
                                             google_api_key=os.environ['GEMINI_KEY'])
        
        self.Llama = ChatGroq(model='gemma2-9b-it',
                              api_key = os.environ['GROQ_KEY'])

    def career_coach(self):
        return Agent(
        role = "Career Coach",
        goal = dedent(f"""\
                    Proporcionar orientación y recomendaciones sobre posibles empleos.
                    evaluar la hoja de vida y la carta de presentación del usuario.
                    desarrollar un plan estratégico para una entrevista laboral exitosa.
                    """),
        backstory = dedent(f"""\
                    Un profesional experimentado en:
                    Asesoramiento de carrera.
                    Búsqueda de empleo.
                    Optimización de hojas de vida y redacción de cartas de presentación.
                    Preparación para entrevistas.
                    """),
        tools = [SearchTool.search_internet],
        verbose = 1,
        llm=self.Gemini,
        max_rpm=2

    )

    def job_search_analyst(self):
        return Agent(
        role = "Job Search Analyst",
        goal = "Investigar y identificar ofertas laborales que se ajusten al perfil y objetivos profesionales del usuario, asegurando la autenticidad y calidad de las oportunidades encontradas",
        backstory = dedent(f"""\
                    Un analista experto en:
                    Búsqueda de empleos en internet y portales de empleo.
                    Identificar oportunidades laborales de calidad.
                    Detectar posibles fraudes o anuncios engañosos.
                    """),
        tools = [SearchTool.search_scrape_google_jobs, SearchTool.search_internet, SearchTool.scrape_website],
        verbose = 1,
        llm=self.Llama,
        max_rpm=2
    )
    
    def cv_writer(self):
        return Agent(
        role = "Escritor y Evaluador de Hojas de Vida",
        goal = dedent(f"""\
                    Crear y revisar hojas de vida y cartas de presentación personalizadas
                    Aliner el perfil profesional del usuario y las ofertas laborales identificadas por el Job Search Analyst.
                    """),
        backstory = "Un escritor altamente calificado en creación de hojas de vida y cartas de presentación. con experiencia en adaptar estos documentos para maximizar la oportunidad de obtener entrevistas.",
        #tools = [],
        verbose = 1,
        llm=self.Gemini,
        max_rpm=2
    )

    def cv_analyst(self):
        return Agent(
            role="Analista de hojas de vida",
            goal="Realizar un resumen de la hoja de vida del usuario, con el fin de permitir una busqueda de calidad de las ofertas laborales",
            backstory = dedent(f"""
                Revisor de hojas de vida.
                Se encarga de resumir la hoja de vida del usuario y extraer información necesaria para realizar la busqueda de ofertas laborales 
                """),
            verbose=1,
            llm=self.Llama,
            max_rpm=2
        )