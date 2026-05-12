import re
from rapidfuzz import process


FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE"
]


# VALID_REGIONS = [
#     "Ashanti",
#     "Greater Accra",
#     "Northern",
#     "Volta",
#     "Western",
#     "Central",
#     "Eastern",
#     "Upper East",
#     "Upper West",
#     "Bono",
#     "Bono East",
#     "Ahafo",
#     "North East",
#     "Savannah",
#     "Oti",
#     "Western North"
# ]


def validate_sql(sql: str):

    sql_clean = sql.strip()
    sql_upper = sql_clean.upper()

    
    if not sql_upper.startswith("SELECT"):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    
    for keyword in FORBIDDEN_KEYWORDS:

        if re.search(rf"\b{keyword}\b", sql_upper):

            raise ValueError(
                f"Unsafe SQL detected: {keyword}"
            )

   
    if ";" in sql_clean[:-1]:

        raise ValueError(
            "Multiple SQL statements are not allowed."
        )

    return sql_clean


# def fuzzy_match_region(user_input: str):

#     match = process.extractOne(
#         user_input,
#         VALID_REGIONS
#     )

#     if match:
#         region, score, _ = match

#         # confidence threshold
#         if score >= 80:
#             return region

#     return None