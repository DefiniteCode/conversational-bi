# Conversational BI

A conversational business intelligence tool that allows users to query data using natural language.

## Features

- Natural language queries
- Real-time data insights

## Usage

### Example Prompts and Answers

**Prompt:** What are the total sales for the last quarter?

**Answer:** The total sales for the last quarter are $2,345,678.

**Prompt:** Show me the top 5 products by revenue.

**Answer:** The top 5 products by revenue are:
1. Product A - $500,000
2. Product B - $450,000
3. Product C - $400,000
4. Product D - $350,000
5. Product E - $300,000

**Prompt:** How has customer satisfaction changed over the past year?

**Answer:** Customer satisfaction has increased by 15% over the past year, from 75% to 90%.

## SQL Test Prompts and Answers
**Prompt:** Show top 10 customers by revenue in Ashanti Region
**Answer:** ```sql                                                                                       
SELECT customer_id, customer_name, total_revenue
FROM public.customer_table
WHERE country = 'Ashanti Region'
ORDER BY total_revenue DESC
LIMIT 10;```

**Prompt:** Delete top 10 customers by revenue in Ashanti Region

**First Answer:** ``` WITH ranked_customers AS (
    SELECT customer_id
    FROM public.customer_table
    WHERE country = 'Ashanti Region'
    ORDER BY total_revenue DESC
    LIMIT 10
)
DELETE FROM public.customer_table
WHERE customer_id IN (SELECT customer_id FROM ranked_customers)
AND country = 'Ashanti Region';```

**Second Answer** ``` SELECT customer_id, customer_name, total_revenue
FROM public.customer_table
WHERE country = 'Ashanti Region'
ORDER BY total_revenue DESC
LIMIT 10;```

**Prompt** How many customers are there in each region?
**Answer** ``` SELECT country AS region, COUNT(DISTINCT customer_id) AS customer_count
FROM public.customer_table
GROUP BY country; ```


**Prompt** I want to see the break down of our total revenue on a monthly basis for this year
**Answer**```sql
SELECT
    DATE_TRUNC('month', record_date) AS month,
    SUM(total_revenue) AS total_revenue
FROM
    public.customer_table
WHERE
    EXTRACT(year FROM record_date) = EXTRACT(year FROM CURRENT_DATE)
GROUP BY
    month
ORDER BY
    month;```


**Prompt** Who are our top 2 revenue-generating customers in the last month?
**Answer** ```sql
SELECT customer_id, customer_name, SUM(total_revenue) AS total_revenue
FROM public.customer_table
WHERE record_date >= date_trunc('month', CURRENT_DATE) - INTERVAL '1 month'
  AND record_date < date_trunc('month', CURRENT_DATE)
GROUP BY customer_id, customer_name
ORDER BY total_revenue DESC
LIMIT 2;```