from dotenv import load_dotenv
from openai import OpenAI
from validations import validate_sql
load_dotenv()

client = OpenAI()


def ask_chatgpt(user_question):

    system_prompt = """
        You are a SQL generator for a conversational BI system.

        Database table: public.customer_table

        Schema:
        record_date DATE
        - Date the transaction or purchase was recorded.

        customer_id VARCHAR
        - Unique identifier for each customer.
        - Example: C001

        customer_name VARCHAR
        - Full name of the customer.
        - Example: Ama Mensah

        age INTEGER
        - Customer age.
        - Example: 28

        gender VARCHAR
        - Customer gender.
        - Values:
        - M = Male
        - F = Female

        city VARCHAR
        - Customer city location.
        - Example values:
        - Accra
        - Kumasi
        - Takoradi

        state VARCHAR
        - Customer region/state in Ghana.
        - IMPORTANT:
        - Values do NOT contain the word "Region".
        - Example:
            "Greater Accra"
            NOT "Greater Accra Region"

        - Example values:
        - Greater Accra
        - Ashanti
        - Western
        - Northern
        - Volta
        - Eastern
        - Central

        country VARCHAR
        - Country name.
        - Example:
        - Ghana

        segment VARCHAR
        - Customer/business segment classification.

        - Example values:
        - Retail
        - SME
        - Corporate
        - Wholesale

        product_category VARCHAR
        - Product or service category purchased.

        - Example values:
        - Airtime
        - Data Bundle
        - Bulk SMS
        - Broadband
        - Voice Package

        quantity_purchased INTEGER
        - Quantity of product/service purchased.

        - Example:
        - 2
        - 5
        - 120

        unit_price NUMERIC
        - Price per single unit purchased.

        - Example:
        - 10
        - 2
        - 0.05

        total_revenue NUMERIC
        - Total revenue generated from the transaction.
        - Usually:
        quantity_purchased times unit_price

        payment_method VARCHAR
        - Payment method used by the customer.

        - Example values:
        - Mobile Money
        - Card
        - Invoice
        - Cash
        - Bank Transfer

        orders_count INTEGER
        - Number of orders made by the customer.

        last_purchase_time TIMESTAMP
        - Timestamp of the customer's latest purchase activity.
        - Example:
        - 2026-05-01 08:10:00


        SQL Generation Rules:

        1. Output ONLY valid PostgreSQL SQL.
        2. Never include explanations or markdown.
        3. Only generate SELECT queries.
        4. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or TRUNCATE statements.
        5. Always use public.customer_table.
        6. Use ONLY the columns provided in the schema.
        7. Always use ILIKE for text filtering to support case-insensitive searches.
        8. The state column stores only raw region names without the word "Region".
        Example:
        - Correct: 'Greater Accra'
        - Incorrect: 'Greater Accra Region'
        9. Use LIMIT 100 unless aggregation or ranking is explicitly requested.
        10. Never hallucinate column names or tables.
        11. Prefer readable SQL formatting.

        Intent rules:
        - If user asks for data, records, customers, or filtering , return row-level SELECT query.
        - If user asks for totals, averages, counts, top, bottom, ranking, trends , top/bottom performers or summaries, use aggregation functions.
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


sql_query = ask_chatgpt("How many customers are in Vilta region")
safe_sql_query = validate_sql(sql_query)
print(safe_sql_query)