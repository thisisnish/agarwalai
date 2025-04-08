from crewai.flow.flow import Flow, listen, start, after_kickoff, before_kickoff
from pydantic import BaseModel
from mechanic_agent_hub.crews.jeep_wrangler_2017.jeep_wrangler_2017 import JeepWrangler2017
import openai

AGENTS = {
    "jeep-wrangler-2017": JeepWrangler2017(),
}


class State(BaseModel):
    query: str = ""
    solution: str = ""
    make: str = ""
    model: str = ""
    year: str = ""
    agent: object = ""
    image_url: str = ""


class MechanicAssistantFlow(Flow[State]):
    """Mechanic Assistant Flow"""

    @start()
    def get_query(self):
        """Get the query from the user."""
        self.state.make = input("What is the make of your car? ")
        self.state.model = input("What is the model of your car? ")
        self.state.year = input("What is the year of your car? ")
        self.state.query = input("What is your query? ")

        print(
            f"\n Searching for assistance for {self.state.make} {self.state.model} {self.state.year}..."
        )
        self.state.agent = AGENTS.get(
            f"{self.state.make.lower()}-{self.state.model.lower()}-{self.state.year}",
            None,
        )

        if not self.state.agent:
            print(
                f"Sorry, we don't have assistance for {self.state.make} {self.state.model} {self.state.year}."
            )
            return self.end()

        return self.state

    @listen(get_query)
    def extract_image_text(self):
        """Extract text from the image."""
        self.state.image_url = input("What is the image URL? ")
        return self.state

    @listen(extract_image_text)
    def research_user_query(self):
        """Research the user query."""
        result = self.state.agent.crew().kickoff(
            inputs={"query": self.state.query, "image_url": self.state.image_url}
        )
        print(
            f"\n Result for {self.state.make} {self.state.model} {self.state.year}: {result}"
        )
    
    @after_kickoff
    def cleanup_openai_clients(self):
        try:
            from openai import OpenAI
            OpenAI().close()
        except Exception:
            pass
    
    @before_kickoff
    def setup_openai_clients(self):
        try:
            from openai import OpenAI
            OpenAI().setup()
        except Exception:
            pass


def kickoff():
    """Kickoff the flow."""
    """Kickoff the flow."""
    try:
        MechanicAssistantFlow().kickoff()
    finally:
        try:
            openai.OpenAI().close()
        except Exception:
            pass

def plot():
    """Plot the flow."""
    flow = MechanicAssistantFlow()
    flow.plot("mechanic_assistant_flow")

if __name__ == "__main__":
    kickoff()
    plot()
