from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai_tools import (
    VisionTool,
    YoutubeVideoSearchTool,
)

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class JeepWrangler2017():
    """JeepWrangler2017 crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    knowledge_base = PDFKnowledgeSource(
        file_paths=['data/jeep_wrangler_2017.pdf'],
        name='Jeep Wrangler 2017',
        description='Jeep Wrangler 2017 PDF',
    )

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            knowledge_sources=[self.knowledge_base],
            memory=True,
            tools=[YoutubeVideoSearchTool()],
            short_term_memory=ShortTermMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="short_term",
                    path="data/memory/jeep_wrangler_2017_short_term_memory/",
                ),
            ),
            long_term_memory=LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="data/memory/jeep_wrangler_2017_long_term_memory.db",
                ),
            ),
            entity_memory=EntityMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="entity",
                    path="data/memory/jeep_wrangler_2017_entity_memory/",
                )
            )
        )

    @agent
    def image_text_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config['image_text_extractor'],
            verbose=True,
            tools=[VisionTool()],
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            output_file='research.json',
        )

    @task
    def text_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config['text_extraction_task'],
            output_file='text_extraction_task.json'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the JeepWrangler2017 crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
