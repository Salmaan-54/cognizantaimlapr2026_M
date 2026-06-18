from urllib import response

from langchain_core import env
from langchain_openai import ChatOpenAI, data
from langchain_classic.agents import initialize_agent, Tool, AgentType
import requests
import os
import json
import re
import smtplib
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), "..",".env")
load_dotenv(env_path)
API_URL = os.getenv("api_url")
ORDER_API_URL = os.getenv("order_api_url")


EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "zoho").lower()

IMAP_SERVERS = {
    "gmail": "imap.gmail.com",
    "outlook": "outlook.office365.com",
    "zoho": "imap.zoho.in"
}

imap_server = IMAP_SERVERS[EMAIL_PROVIDER]


def food_delivery_policy_search_tool(question: str) -> str:
    response = requests.post(
        API_URL,
        json={"prompt": question}
    )

    print(response.status_code)
    print(response.text)

    response.raise_for_status()

    data = response.json()
    return data.get("answer", "No answer found")
#Create an order for Parameswari, product id 128, product name TV, Quantity 1, Price 50000
def save_order_to_db_tool(order_details: str) -> str:
    try:
        parts = [x.strip() for x in order_details.split(",")]

        if len(parts) != 5:
            return (
                "Invalid input format.\n"
                "Expected: customer_name,product_id,product_name,quantity,price\n"
                "Example: Vignesh,101,Refrigerator,1,70000"
            )

        customer_name, product_id, product_name, quantity, price = parts

        missing_fields = []

        if not customer_name:
            missing_fields.append("customer_name")

        if not product_id:
            missing_fields.append("product_id")

        if not product_name:
            missing_fields.append("product_name")

        if not quantity:
            missing_fields.append("quantity")

        if not price:
            missing_fields.append("price")

        if missing_fields:
            return (
                f"Missing required field(s): "
                f"{', '.join(missing_fields)}"
            )

        payload = {
            "customer_name": customer_name,
            "product_id": int(product_id),
            "product_name": product_name,
            "quantity": int(quantity),
            "price": float(price)
        }

        print("Payload:", payload)

        response = requests.post(ORDER_API_URL, json=payload)
        response.raise_for_status()

        data = response.json()

        return (
            f"✅ Order saved successfully\n\n"
            f"Payload Sent:\n{payload}\n\n"
            f"API Response:\n{data}"
        )

    except ValueError as e:
        return (
            "Invalid numeric value.\n"
            "product_id and quantity must be integers.\n"
            "price must be numeric.\n"
            f"Error: {str(e)}"
        )

    except requests.exceptions.RequestException as e:
        return f"Order API error: {str(e)}"

    except Exception as e:
        return f"Unexpected error: {str(e)}"

def email_order_confirmation(customer_data) -> str:

    try:

        # If input is string, convert to dict
        if isinstance(customer_data, str):

            parts = [x.strip() for x in customer_data.split(",")]

            if len(parts) != 6:
                return (
                    "Invalid input format.\n"
                    "Expected:\n"
                    "customer_name,product_id,product_name,quantity,price,customer_email"
                )

            customer_data = {
                "customer_name": parts[0],
                "product_id": int(parts[1]),
                "product_name": parts[2],
                "quantity": int(parts[3]),
                "price": float(parts[4]),
                "customer_email": parts[5]
            }

        recipient_email = customer_data.get("customer_email")

        if not recipient_email:
            return "Customer email is missing."

        sender_email = EMAIL_USER
        sender_password = EMAIL_PASSWORD

        subject = "Order Confirmation"

        body = f"""
            Dear {customer_data.get('customer_name')},

            Your order has been successfully placed.

            Order Details:
            Product ID: {customer_data.get('product_id')}
            Product Name: {customer_data.get('product_name')}
            Quantity: {customer_data.get('quantity')}
            Price: {customer_data.get('price')}

            Regards,
            Food Delivery Support Team
            """

        with smtplib.SMTP_SSL("smtp.zoho.in", 465) as server:
            server.login(sender_email, sender_password)

            message = f"Subject: {subject}\n\n{body}"

            server.sendmail(
                sender_email,
                recipient_email,
                message
            )

        return (
            f"✅ Order confirmation email sent successfully to "
            f"{recipient_email}"
        )

    except Exception as e:
        return f"❌ Failed to send email: {str(e)}"



tools = [
    Tool(
        name="FoodDeliveryPolicySearch",
        func=food_delivery_policy_search_tool,
        description="Use this to answer food delivery policy questions from the RAG knowledge base."
    ),
    Tool(
        name="SaveOrderToDB",
        func=save_order_to_db_tool,
        description="""
        Use this tool to save customer orders.

        Input format:
        customer_name,product_id,product_name,quantity,price

        Example:
        Parameswari,123,TV,1,50000
        """
            ),

        Tool(
        name="EmailOrderConfirmation",
        func=email_order_confirmation,
        description="""
        Use this tool to send order confirmation emails to customers.

        Input format:
        customer_name,product_id,product_name,quantity,price,customer_email,

        Example:
        Parameswari,123,TV,1,50000,example@example.com
        """
            )
        ]


def create_food_delivery_agent():
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
            You are an Food Delivery Assistant Agent.

            Use tools carefully.

            Rules:
            - Select only one best tool.
            - Do not repeat tool calls.
            - After tool result, return Final Answer.
            - FoodDeliveryPolicySearch: use for food delivery policy questions.
            - SaveOrderToDB: use for saving order details to the database.            
            """
        }
    )

    return agent


def ask_food_delivery_agent(question: str):
    agent = create_food_delivery_agent()

    response = agent.invoke({
        "input": question
    })

    return {
        "answer": response["output"]
    }