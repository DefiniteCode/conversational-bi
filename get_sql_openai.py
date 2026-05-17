from dotenv import load_dotenv
from openai import OpenAI
from validations import validate_sql
from prompts import system_prompt, reinforncement_prompt
import logging

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

client = OpenAI()

system_prompt = system_prompt

def ask_chatgpt(user_question):
    
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


def ask_chatgpt_validated(user_question: str, max_retries: int = 2) -> str:
    """Ask the model and validate the SQL. If validation fails due to forbidden
    keywords or non-SELECT statements, re-prompt the model with a strict
    instruction to return only a safe SELECT query. Retries up to
    `max_retries` times before raising the last validation error.
    """
    logger.info(f"ask_chatgpt_validated called with user_question: {user_question[:100]}...")
    logger.info(f"Max retries allowed: {max_retries}")

    def call_model(user_prompt: str) -> str:
        logger.debug(f"Calling OpenAI model with prompt: {user_prompt[:80]}...")
        resp = client.responses.create(
            model="gpt-4.1-mini",
            temperature=0,
            input=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )
        generated_sql = resp.output_text
        logger.info(f"Model generated SQL: {generated_sql}")
        return generated_sql

    current_prompt = user_question
    last_error = None

    for attempt in range(max_retries + 1):

        logger.info(f"--- Attempt {attempt + 1}/{max_retries + 1} ---")

        sql = call_model(current_prompt)

        try:
            logger.info(f"Validating SQL: {sql}")

            validate_sql(sql)

            logger.info("✓ SQL validation passed! Returning safe query.")

            return sql
        
        except ValueError as e:

            logger.warning(f"✗ Validation failed: {str(e)}")
            last_error = e

            if attempt == max_retries:
                logger.error(f"Max retries ({max_retries}) exceeded. Raising final validation error.")
                raise

            reinforcement= (
                reinforncement_prompt,
                "User request: " + user_question
            )
            logger.info(f"Retrying with reinforcement prompt (attempt {attempt + 2}/{max_retries + 1})...")

            current_prompt = reinforcement


sql_query = ask_chatgpt_validated("what revenue line is the lowest for customers less than 30 years ")
print(sql_query)