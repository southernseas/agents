# Engineering Team Crew Extension

Welcome to the EngineeringTeam Crew project from agents project,
0. requirenents are listed in main.py

## 1. new agents/tasks
a plus busimess analyst agent/task - 1st task
b - add technical writer as last task

## 2. mix of llms - plus agent calls to 
NEED GROQ KEY
a)  llm: groq/moonshotai/kimi-k2-instruct
b) llm: groq/qwen/qwen3-32b
c)) llm: openai/gpt-oss-120b
d) 

## 3. expamded business requirements
a. add screen with current share price of shaare subset.
b. add screen with current bond interest rates
c. add news screen

## agents are :
- (** new***  - business analyst - creates accounts.detailed_requirements.md based on high level requirements in main.py - 
- lead engineer - reads detailed requirements and produces .. accounts.design.md
- backend engineer
- frontend engineer
- unit test engineer
- ***new*** technical writer
powered by [crewAI](https://crewai.com). 

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.



Next, navigate to your project directory and install the dependencies:


To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the engineering_team Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The engineering_team Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the EngineeringTeam Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
