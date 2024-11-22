from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from ai_researcher.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
import os
# os.environ["SERPER_API_KEY"] = "022458ad6f9f70a2369be0041c79f38cd5d87be2"
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool
# search_tool = SerperDevTool()
scraper_tool = ScrapeWebsiteTool(website_url='https://content.naic.org/glossary-insurance-terms')

website_rag_tool = WebsiteSearchTool(
    config=dict(
        llm=dict(
            provider="azure_openai", # or google, openai, anthropic, llama2, ...
            # config=dict(
            #     model="gpt-35-turbo",
            #     # temperature=0.5,
            #     # top_p=1,
            #     # stream=true,
            # ),
        ),
        embedder=dict(
            provider="azure_openai", # or openai, ollama, ...
            config=dict(
                model="text-embedding-ada-002",
                # task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    ),
    website="https://content.naic.org/glossary-insurance-terms"
)


@CrewBase
class AiResearcher():
	"""AiResearcher crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	


	@agent
	def chatbot(self) -> Agent:
		return Agent(
			config=self.agents_config['chatbot'],
			verbose=True
		)

	@agent
	def scraper(self) -> Agent:
		return Agent(
			config=self.agents_config['scraper'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			tools=[website_rag_tool],
			verbose=True
		)

	@agent
	def query_resolver(self) -> Agent:
		return Agent(
			config=self.agents_config['query_resolver'],
			verbose=True
		)


	# @agent
	# def verifier(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['verifier'],
	# 		tools=[search_tool],
	# 		verbose=True
	# 	)


	@task
	def chatbot_task(self) -> Task:
		return Task(
			config=self.tasks_config['chatbot_task'],
			human_input=True,
		)

	@task
	def scraping_task(self) -> Task:
		return Task(
			config=self.tasks_config['scraping_task'],
		)

	@task
	def query_resolver_task(self) -> Task:
		return Task(
			config=self.tasks_config['query_resolver_task'],
			output_file='answer.md'
		)

	# @task
	# def verifier_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['verifier_task'],
	# 		output_file='verified.md'
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the AiResearcher crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
