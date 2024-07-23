from crewai import Task
from textwrap import dedent

class JobSearchTasks():

    def __tip_section(self):
        return "Si realizas el MEJOR TRABAJO, te daré una comisión de $100.000 dolares"
    
    def analyze_cv(self, agent, preferencias_trabajo, perfil, ubicacion):
        return Task(
            description = dedent(
                f"""\
                **Tarea**: Extraer información de la hoja de vida proporcionada por el usuario para buscar ofertas laborales. Al finalizar enviar la información al job search analyst
                **Descripción**: Tomar la hoja de vida proporcionada por el usuario en el input, resumirla y extraer la siguiente información:
                    - Experiencia laboral
                    - Habilidades
                    - Campos laborales
                    - Posibles tipos de empresas
                **Parametros**:
                    - Hoja de vida: {perfil}
                    - Preferencias de trabajo: {preferencias_trabajo}
                    - Ubicación: {ubicacion}

                **Nota**: Realiza el mejor resumen posible, ya que este va a ser usado por el job search analyst para realizar la busqueda de trabajo. {'self.__tip_section()'}, Buena suerte!
                """
            ),
            agent=agent,
            expected_output=dedent(
                """\
                Resumen de la hoja de vida en el siguiente formato:
                [
                    {
                    'nombre candidato': 'Pepito Perez',
                    'Campo o campos laborales': 'Ingenieria, Medicina...',
                    'Experiencia laboral': 'x años en x empresa, y empresa...',
                    'Habilidades': 'Python, Data Science...',
                    'Conocimientos': 'Analisis de datos, Inteligencia artificial...',
                    'Habilidades blandas': 'Responsable, ...',
                    'Ubicación':'Bogotá...'
                    },
                    {{...}}
                ]
                """
            ),
            async_execution=False
        )
    
    def find_jobs(self, agent, perfil, preferencias_trabajo, ubicacion, context):
        return Task(
            description = dedent(
        f"""\
            **Tarea**:
            Buscar dos ofertas relevantes, usando las preferencias de empleo y el resumen de la cv proporcionado por el cv analyst. 
            Al finalizar agregar la información al archivo markdown
            **Descripción**:
            Buscar e identificar dos ofertas laborales que estén acordes con el perfil del usuario y sus preferencias de trabajo y campos relacionados, además de la ubicacion proporcionada. 
            Las industrias relacionadas las puedes estimar de acuerdo a la experiencia laboral. Esto incluye analizar el resumen de hv/cv del usuario proporcionada por tus compañeros. 
            Debes buscar en diferentes portales de empleo y páginas de compañias relacionadas con el perfil del usuario. 
            Se debe asegurar que las ofertas laborales sean reales y no fraudulentas.
            Una vez se encuentren ofertas relevantes, el agente debe compilarlas en una lista y realizar un breve resumen de cada oferta, incluyendo el nombre de la posición, nombre de la compañía, ubicación, responsabilidades, requisitos, salario y el link de la oferta.
            En caso de no poder encontrar las responsabilidades, requisitos, salario o link de la oferta se puede entregar el nombre de la oferta, la empresa y en que portal de empleo se encontró
            **Información a usar**:
            - Resumen del perfil generado por el cv analyzer
            - En caso de ser necesario, esta es la hoja de vida del usuario {perfil}
            - Las preferencias de empleo del usuario son {preferencias_trabajo}
            - Recuerda buscar trabajos en la ubicación seleccionada por el usuario {ubicacion}
            **Nota**: Enfocate en buscar oportunidades de alta calidad y que esten muy relacionadas con el perfil del usuario y sus objetivos laborales. {self.__tip_section()}, Buena suerte!
        """
            ),
            agent=agent,
            expected_output = dedent(
                """\
                Lista de 4 empleos disponibles acordes con las preferencias de trabajo del usuario.
                La lista debe ir de la siguiente manera:
                [
                    {
                    'nombre candidato': 'Pepito Perez',
                    'Campo o campos laborales': 'Ingenieria, Medicina...',
                    'Experiencia laboral': 'x años en x empresa, y empresa...',
                    'Habilidades': 'Python, Data Science...',
                    'Conocimientos': 'Analisis de datos, Inteligencia artificial...',
                    'Habilidades blandas': Responsable, ...,
                    'Ubicación':'Bogotá...'
                    },
                    {
                    'Nombre de la empresa': 'Redbull F1',
                    'Posición':'Analista de datos',
                    'Salario':'$3000000 (Si no se encuentra dejar vacio)',
                    'Ubicación':'Bogotá',
                    'Resumen de la oferta': 'analista de datos con x años de experiencia...(Si no se encuentra dejar vacio)',
                    'Link de la oferta': 'https://... (si no se encuentra, decir que portal de empleo se usó'
                    },
                    {
                    'Nombre de la empresa': 'Empresa 2',
                    'Posición':'...',
                    'Salario':'...',
                    'Ubicación':'...',
                    'Resumen de la oferta': '...',
                    'Link de la oferta': '...'
                    }
                    {{...}}
                ]
                """
            ),
            async_execution=False,
            context=context
        )
    
    def create_custom_resume_and_cover_letter(self, agent, perfil, context, callback_func):
        return Task(
            description = dedent(
            f"""
            **Tarea**: Escribir la hv/cv especifica y carta de presentación para cada oferta. Al finalizar agregar la información al archivo markdown generado
            **Descripción**:
            Crear una hoja de vida o cv personalizada para el usuario de acuerdo a su perfil laboral compartido inicialmente y a las ofertas encontradas por el Job Search Analyst.
            Resaltar las habilidades relevantes, experiencias y logros que estén acordes con los requerimientos de la posición.
            La hoja de vida y carta de presentación deben ser escritas de manera profesional, sin errores
            La hoja de vida debe pasar por un filtro ATS. 
            Se debe asegurar que los documentos esten alineados con las buenas prácticas para aplicar a trabajos
            **Parámetros**:
            - Resumen cv generado por el cv analyzer
            - Ofertas encontradas por el job search analyst
            - Esta es la hoja de vida original del usuario: {perfil}
            **Nota**: 
            Enfocate en crear una buena relación entre las habilidades del usuario y los objetivos de la posición para incrementar las posibilidades de asegurar una entrevista. 
            Presta atención al lenguaje y tono usado en los documentos, para asegurar que sean profesionales y atractivos. 
            De igual manera, asegurate de que ambos documentos se vean que fueron escritos por un humano y no por una IA. 
            Recuerda que la hoja de vida del usuario fue compartida al job search analyst para ser analizada. 
            No es necesario que busques una manera de subir las hojas de vida desarrolladas ya que estas se agregarán al archivo markdown generado
            {self.__tip_section()}, Buena suerte!
            """
            ),
            agent=agent,
            expected_output = dedent(
                """
                Un Curriculum y carta de presentación para cada una de las ofertas encontradas. 
                Ejemplo del resultado:
                [
                    {
                    'nombre candidato': 'Pepito Perez',
                    'Campo o campos laborales': 'Ingenieria, Medicina...',
                    'Experiencia laboral': 'x años en x empresa, y empresa...',
                    'Habilidades': 'Python, Data Science...',
                    'Conocimientos': 'Analisis de datos, Inteligencia artificial...',
                    'Habilidades blandas': Responsable, ...,
                    'Ubicación':'Bogotá...'
                    },
                    {
                    'Nombre de la empresa': 'Redbull F1',
                    'Posición':'Analista de datos',
                    'Salario':'$3000000 (Si no se encuentra dejar vacio)',
                    'Ubicación':'Bogotá',
                    'Resumen de la oferta': 'analista de datos con x años de experiencia...(Si no se encuentra dejar vacio)',
                    'Link de la oferta': 'https://... (si no se encuentra, decir que portal de empleo se usó'
                    'CV Generada':'Insertar cv generada',
                    'Carta de presentación':'Insertar carta de presentación generada'
                    },
                    {
                    'Nombre de la empresa': 'Empresa 2',
                    'Posición':'...',
                    'Salario':'...',
                    'Ubicación':'...',
                    'Resumen de la oferta': '...',
                    'Link de la oferta': '...',
                    'CV Generada':'...',
                    'Carta de presentación':'...'
                    }
                    {{...}}
                ]
                """
            ),
            async_execution=False,
            context = context,
            callback=callback_func
        )
    
    def provide_job_search_guidance_and_interview_prep(self, agent, context, callback_func):
        return Task(
            description = dedent(
        f"""
            **Tarea**:
            Brindar orientación para la búsqueda de empleo y preparación para las entrevistas.
            Agregar al archivo markdown la información encontrada y la cv y carta de presentación generada. 
            **Descripción**: 
            Proporcionar una guía y recomendaciones integrales para el proceso de entrevista para el usuario. 
            Evaluar el curriculum y la carta de presentación personalizados creados por el CV writter y brindar comentarios para garantizar que estén optimizados para el puesto de trabajo identificado por el Job Search Analyst. 
            Desarrollar un plan estratégico para preparar al usuario para una entrevista de trabajo exitosa, que incluya posibles preguntas y respuestas, consejos sobre el lenguaje corporal y otros consejos relevantes. 
            Agregar todo esto al archivo markdown en el que se recopila toda la información encontrada y generada.
            **Parametros**:
            - CV y carta de presentación generados por el cv writer de acuerdo a las ofertas encontradas
            **Nota**:
            Enfocate en brindar asesoramiento práctico y personalizado que se ajuste a los objetivos profesionales del usuario y a los requisitos del puesto. 
            Asegurate de que el usuario se sienta seguro y preparado para su entrevista de trabajo, ofreciéndole consejos prácticos y abordando cualquier inquietud que pueda tener. 
            {self.__tip_section()}, buena suerte!
        """
            ),
            agent=agent,
            context = context,
            expected_output = dedent(
                """
                Se espera el siguiente resultado:
                [
                    {
                    'nombre candidato': 'Pepito Perez',
                    'Campo o campos laborales': 'Ingenieria, Medicina...',
                    'Experiencia laboral': 'x años en x empresa, y empresa...',
                    'Habilidades': 'Python, Data Science...',
                    'Conocimientos': 'Analisis de datos, Inteligencia artificial...',
                    'Habilidades blandas': Responsable, ...,
                    'Ubicación':'Bogotá...'
                    },
                    {
                    'Nombre de la empresa': 'Redbull F1',
                    'Posición':'Analista de datos',
                    'Salario':'$3000000 (Si no se encuentra dejar vacio)',
                    'Ubicación':'Bogotá',
                    'Resumen de la oferta': 'analista de datos con x años de experiencia...(Si no se encuentra dejar vacio)',
                    'Link de la oferta': 'https://... (si no se encuentra, decir que portal de empleo se usó'
                    'CV Generada':'Insertar cv generada',
                    'Carta de presentación':'Insertar carta de presentación generada',
                    'Consejos entrevista':'Información necesaria para prepararse para la entrevista'
                    },
                    {
                    'Nombre de la empresa': 'Empresa 2',
                    'Posición':'...',
                    'Salario':'...',
                    'Ubicación':'...',
                    'Resumen de la oferta': '...',
                    'Link de la oferta': '...',
                    'CV Generada':'...',
                    'Carta de presentación':'...',
                    'Consejos entrevista':'Información necesaria para prepararse para la entrevista'
                    }
                    {{...}}
                ]
                """
            ),
            async_execution=False,
            callback=callback_func
        )
    
    def compilador_archivo(self, agent, context, callback_func):
        return Task(
            description = dedent(
                f"""\
                Compilar la lista en un archivo markdown organizado por secciones sin perder la información generada.
                El archivo markdown debe ir organizado de la misma manera en la que se recibe la información.
                """
            ),
            agent=agent,
            context=context,
            async_execution=False,
            callback=callback_func,
            expected_output=dedent(
                """\
                Archivo markdown organizado de la siguiente manera:

                # Trabajos encontrados
                ## Resumen Candidato
                nombre candidato: Pepito Perez,
                Campo o campos laborales: Ingenieria, Medicina...,
                Experiencia laboral: 'x años en x empresa, y empresa...,
                Habilidades: Python, Data Science...,
                Conocimientos: Analisis de datos, Inteligencia artificial...,
                Habilidades blandas: Responsable, ...,
                Ubicación:Bogotá...

                ## Ofertas encontradas

                ###Nombre de la empresa: Redbull F1,
                Posición:Analista de datos,
                Salario:$3000000 (Si no se encuentra dejar vacio),
                Ubicación:Bogotá,
                Resumen de la oferta: analista de datos con x años de experiencia...(Si no se encuentra dejar vacio),
                Link de la oferta: https://... (si no se encuentra, decir que portal de empleo se usó
                ####CV Generada
                Insertar cv generada,
                ####Carta de presentación
                Insertar carta de presentación generada,
                ####Consejos entrevista
                Información necesaria para prepararse para la entrevista

                ###Nombre de la empresa': 'Empresa 2',
                Posición:...
                Salario:...
                Ubicación:...
                Resumen de la oferta:...
                Link de la oferta:...
                ####CV Generada
                ...
                ####Carta de presentación
                ...
                ####Consejos entrevista
                Información necesaria para prepararse para la entrevista
                """
            )
        )