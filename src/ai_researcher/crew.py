from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool, PDFSearchTool
from dotenv import load_dotenv
import os

load_dotenv()


# Tools for web scraping and website search
# scraper_tool = ScrapeWebsiteTool(website_url='https://content.naic.org/glossary-insurance-terms')
# website_rag_tool = WebsiteSearchTool(
#     config=dict(
#         llm=dict(
#             provider="azure_openai",
#             config=dict(
#                 model="gpt-35-turbo"
#             )#         ),
#         embedder=dict(
#             provider="azure_openai",
#             config=dict(model="text-embedding-ada-002"),
#         ),
#     ),
#     website="https://content.naic.org/glossary-insurance-terms"
# )
# pdf_search_tool = PDFSearchTool(
#     pdf="uploaded_files/uploaded.pdf",
#     config=dict(
#         llm=dict(
#             provider="azure_openai",
#             config=dict(
#                 model="gpt-35-turbo"
#             )
#         ),
#         embedder=dict(
#             provider="azure_openai",
#             config=dict(model="text-embedding-ada-002"),
#         )
#     )
# )

@CrewBase
class PolicyAgenticRAG:
    """PolicyAgenticRAG Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def step_callback(output):
        print(f"output: {output}")

    def create_pdf_search_tool(self):
        pdf_search_tool = PDFSearchTool(
            pdf="uploaded_files/uploaded.pdf",
            config=dict(
                llm=dict(
                    provider="azure_openai",
                    config=dict(
                        model="gpt-35-turbo"
                    )
                ),
                embedder=dict(
                    provider="azure_openai",
                    config=dict(model="text-embedding-ada-002"),
                )
            )
        )
        return pdf_search_tool
    # pdf_search_tool = PDFSearchTool(
    #     pdf="uploaded_files/uploaded.pdf",
    #     config=dict(
    #         llm=dict(
    #             provider="azure_openai",
    #             config=dict(
    #                 model="gpt-35-turbo"
    #             )
    #         ),
    #         embedder=dict(
    #             provider="azure_openai",
    #             config=dict(model="text-embedding-ada-002"),
    #         )
    #     )
    # )

    @agent
    def scraper(self) -> Agent:
        return Agent(config=self.agents_config['scraper'], tools=[self.create_pdf_search_tool()], verbose=True)

    @agent
    def query_resolver(self) -> Agent:
        return Agent(config=self.agents_config['query_resolver'], verbose=True)

    @task
    def scraping_task(self) -> Task:
        return Task(config=self.tasks_config['scraping_task'])

    @task
    def query_resolver_task(self) -> Task:
        return Task(config=self.tasks_config['query_resolver_task'], output_file='answer.md')

    
    
    @crew
    def crew(self) -> Crew:
        """Creates the PolicyAgenticRAG Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
