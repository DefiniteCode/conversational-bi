from google import genai

client = genai.Client(api_key="AIzaSyDHynVPB-iKpXNgiJ0Lmqw083Ab8N_TbF8")

def ask_gemini(prompt: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

user_prompt = "I need base of customers in Ashanti Region"

master_prompt = """
You are a SQL generator for a conversational BI system.

Database table: public.customer_table

Schema:
record_date date
customer_id character varying
customer_name character varying
age integer
gender character varying
city character varying
state character varying (the content have no 'Region' keyword attached so just the region name)
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

Intent rules:
- If user asks for data, records, customers, or filtering → return row-level SELECT query.
- If user asks for totals, averages, counts, top, bottom, ranking, or trends → use aggregation.
- If unclear → default to row-level SELECT query.

User question:
{user_prompt}
"""
print(ask_gemini(master_prompt))





