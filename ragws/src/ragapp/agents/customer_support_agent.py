from langchain_openai import ChatOpenAI
from langchain_classic.agents import initialize_agent, Tool, AgentType

from nlpapp.utils.rag_demo.rag_engine import ask_question


def hr_policy_search_tool(question: str) -> str:
    response = ask_question(question)
    return response["answer"]


def leave_calculator_tool(query: str) -> str:
    """
    Example input: annual leave 20, used 7
    """
    import re

    numbers = list(map(int, re.findall(r"\d+", query)))

    if len(numbers) >= 2:
        total_leave = numbers[0]
        used_leave = numbers[1]
        balance = total_leave - used_leave
        return f"Leave balance is {balance} days."

    return "Please provide total leave and used leave."


def escalation_tool(query: str) -> str:
    return (
        "Escalate unresolved HR issues to Level 1 HR Support first. "
        "If unresolved, escalate to HR Manager with employee ID, issue details, and supporting documents."
    )


def email_draft_tool(query: str) -> str:
    return f"""
Subject: HR Policy Clarification Request

Dear HR Team,

I would like to request clarification regarding the following HR policy matter:

{query}

Kindly review and guide me.

Regards,
Employee
"""


def ticket_creation_tool(query: str) -> str:
    return (
        "HR ticket draft created. Category: HR Policy Support. "
        f"Issue Summary: {query}"
    )


tools = [
    Tool(
        name="HRPolicySearch",
        func=hr_policy_search_tool,
        description="Use this to answer HR policy questions from the RAG knowledge base."
    ),
    Tool(
        name="LeaveCalculator",
        func=leave_calculator_tool,
        description="Use this to calculate leave balance. Input should contain total leave and used leave."
    ),
    Tool(
        name="EscalationAdvisor",
        func=escalation_tool,
        description="Use this when the user asks how to escalate an HR issue."
    ),
    Tool(
        name="HREmailDraft",
        func=email_draft_tool,
       description="""
        Use ONLY when the user asks to draft, write, or compose an email.
        The tool returns the complete final answer.
        DO NOT call any other tool afterward.
        """
    ),
    Tool(
        name="HRTicketCreator",
        func=ticket_creation_tool,
        description="Use this to create an HR support ticket draft."
    )
]


def create_hr_agent():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=3,
        early_stopping_method="generate",
        agent_kwargs={
            "prefix": """
            You are an HR Assistant Agent.

            Use tools carefully.

            Rules:
            - Select only one best tool.
            - Do not repeat tool calls.
            - After tool result, return Final Answer.
            - HRPolicySearch: use for HR policy questions.
            - HREmailDraft: use for drafting emails.
            - EscalationAdvisor: use for escalation questions.
            - LeaveCalculator: use for calculating leave balance.
            - HRTicketCreator: use for creating HR support tickets.
            """
        }
    )

    return agent


def ask_hr_agent(question: str):
    agent = create_hr_agent()

    response = agent.invoke({
        "input": question
    })

    return {
        "answer": response["output"]
    }