# Data Science Project Questionnaire

## 1. Project Overview

*   **What is the primary objective of this project?**
    *   *Answer:* To understand the key drivers of customer churn for our B2B SaaS product and to build a predictive model that can identify at-risk customers at least 30 days before their renewal date.

## 2. Data

*   **What data sources are available?**
    *   *Answer:* We have access to three main tables in the production Databricks environment: `prod_catalog.main.users` (user demographic and firmographic data), `prod_catalog.main.subscriptions` (MRR, plan type, term length, renewal dates), and `support_catalog.main.tickets` (unstructured text from support interactions).
*   **Are there any known data quality issues?**
    *   *Answer:* The `users` table has some null values for `employee_count` and `industry`. The `tickets` data is raw text and will require significant NLP feature engineering.
*   **What are the key variables and column names of interest?**
    *   *Answer:* From `subscriptions`: `user_id`, `mrr`, `plan_type`, `start_date`, `end_date`. From `users`: `company_size`, `industry`, `signup_date`. From `tickets`: `ticket_id`, `creation_ts`, `resolution_status`.

## 3. Analysis

*   **What are the main questions you are trying to answer?**
    *   *Answer:* 1. What user behaviors (e.g., feature usage, support ticket frequency) are most correlated with churn? 2. Is there a specific point in the customer lifecycle where churn risk is highest? 3. Can we build a reliable model to predict churn?
*   **What analytical methods do you want to use? (e.g., regression, classification, clustering)**
    *   *Answer:* Primarily classification models. We will start with a Logistic Regression baseline and then evaluate a Random Forest or Gradient Boosting model for improved performance. Some clustering on user behavior might also be useful for feature engineering.
*   **What are the success criteria for the analysis?**
    *   *Answer:* The primary success criterion is a classification model with an AUC score greater than 0.85 on a held-out test set. A secondary goal is to deliver a ranked list of at least three actionable churn drivers to the product team.

## 4. Technical Details

*   **Are there any specific libraries or frameworks that should be used?**
    *   *Answer:* Standard PyData stack: `scikit-learn` for modeling, `pandas` for data manipulation, `matplotlib`/`seaborn` for visualization. We should use the provided `execute_sql` function for all data extraction. 