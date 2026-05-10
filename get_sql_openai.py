from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def ask_chatgpt(user_question):

    system_prompt = """
        You are a SQL generator for a conversational BI system.

        Database table: public.customer_table

        Schema:
        record_date date
        customer_id character varying
        customer_name character varying
        age integer
        gender character varying
        city character varying
        state character varying
        (country has no 'Region' keyword attached, only the raw region name)
        country character varying
        segment character varying
        product_category character varying
        quantity_purchased integer
        unit_price numeric
        total_revenue numeric
        payment_method character varying
        orders_count integer
        last_purchase_time timestamp without time zone

        Rules:
        1. Output ONLY valid PostgreSQL SQL.
        2. Do not include explanations or formatting.
        3. Always use public.customer_table.
        4. ONLY generate READ-ONLY queries.
        5. NEVER generate:
            - DELETE
            - UPDATE
            - INSERT
            - DROP
            - ALTER
            - TRUNCATE
            - CREATE
            - GRANT
            - REVOKE
        6. If the user asks for destructive or modifying operations,
        return a safe SELECT query instead.
        7. Prefer SELECT statements only.

        Intent rules:
        - If user asks for data, records, customers, or filtering → return row-level SELECT query.
        - If user asks for totals, averages, counts, top, bottom, ranking, or trends → use aggregation.
        - If unclear → default to row-level SELECT query.
        """
    
    response = client.responses.create(
        model="gpt-4.1-mini",
        temperature=0,
        input=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_question
            }
        ]
    )

    return response.output_text


sql_query = ask_chatgpt("Who are our top 2 revenue-generating customers in the last month?")
print(sql_query)