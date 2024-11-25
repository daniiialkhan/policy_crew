from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Optional
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool

# FastAPI App
app = FastAPI()

# Store results for intermediate and final outputs
results: Dict[str, List[Dict]] = {}

# Tools for web scraping and website search
scraper_tool = ScrapeWebsiteTool(website_url='https://content.naic.org/glossary-insurance-terms')
website_rag_tool = WebsiteSearchTool(
    config=dict(
        llm=dict(provider="azure_openai"),
        embedder=dict(
            provider="azure_openai",
            config=dict(model="text-embedding-ada-002"),
        ),
    ),
    website="https://content.naic.org/glossary-insurance-terms"
)

# Input model for FastAPI
class QueryInput(BaseModel):
    query: str


@CrewBase
class AiResearcher:
    """AiResearcher Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def scraper(self) -> Agent:
        return Agent(config=self.agents_config['scraper'], tools=[website_rag_tool], verbose=True)

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
        """Creates the AiResearcher Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


# Step Callback to capture agent outputs
def step_callback(agent, task, output):
    """Callback function to capture intermediate outputs."""
    if task.query not in results:
        results[task.query] = []
    results[task.query].append({
        "agent": agent.role,
        "task": task.description,
        "output": output
    })


@app.post("/start_crew/")
async def start_crew(input: QueryInput, background_tasks: BackgroundTasks):
    """
    Start the Crew process in the background for the given query.
    """
    ai_researcher = AiResearcher()
    crew_instance = ai_researcher.crew()

    # Attach step callback
    crew_instance.step_callback = step_callback

    # Run the crew in the background
    def kickoff_crew():
        crew_instance.kickoff(inputs={"query": input.query})

    background_tasks.add_task(kickoff_crew)
    return {"message": "Crew started successfully.", "query": input.query}


@app.get("/get_results/")
def get_results(query: str):
    """
    Retrieve intermediate and final results for a given query.
    """
    if query in results:
        return {"status": "complete", "outputs": results[query]}
    return {"status": "processing", "outputs": []}
