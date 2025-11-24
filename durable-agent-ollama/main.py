import asyncio
import logging

from dapr_agents import DaprChatClient, DurableAgent  # type: ignore
from dapr_agents.workflow.runners import AgentRunner # type: ignore


async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    llm = DaprChatClient(component_name='ollama')

    durable_agent = DurableAgent(
        role="Personal Assistant",
        name="Stevie",
        goal="Help humans answer any question they may have.",
        instructions=[
            "Respond clearly and helpfully to any question.",
        ],
        llm=llm
    )
    durable_agent.start()
    runner = AgentRunner()

    try:
        prompt = "How can I run ollama locally with Dapr Conversation API and dapr-agents durable agent?"

        result = await runner.run(
            durable_agent,
            payload={"task": prompt},
        )

        print(f"\n✅ Final Result:\n{result}\n", flush=True)

    except Exception as e:
        logger.error(f"Error running workflow: {e}", exc_info=True)
        raise
    finally:
        durable_agent.stop()
        runner.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
