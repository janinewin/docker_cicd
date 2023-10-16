## Goal

As a data engineer, you need to be able to think of a data structure (tables, columns etc) in your data warehouse that's
- not repetitive (similar information is not repetited in many fields or tables)
- easy to read, understand and manipulate for data analysts or scientists

Hence, from very raw and disorganized data extracted from the different systems your company interacts with, the data engineer needs to write scripts to map this unstructured data into a clean and limited set of tables: this is called "Data Modeling". If you are interested more in this topic, you should explore what Analytics Engineers do!

The exercise is split in 2 parts:
1. A high level business question
2. An underlying design question

❓You have to think of a data structure that would be optimized for the business, and would enable the data analyst to, in a simple query on top of those tables, answer the business question that is asked.

Hence there will be 2 deliverables:
- an ERD Diagram that shows the structure of tables the student has in mind. And its equivalent DDL (aka : the SQL script that - when executed in Postgres - enables you to create the structure you just laid out)
- the SQL query to answer the business question

## Tasks

You work in **Company ABC**, which sells products online.

The marketing team would like to, everyday, push to their CRM the list of all their customers, with their first name, last name, and email address, with some attributes related to their behavior:
- the total number of orders they've made
- the total amount of money they spent
- the product they purchased the most
... so that they can efficiently target them.

Note that orders can be either "completed", or "canceled".

1. **❓ Provide the underlying MINIMALISTIC raw database structure and relationships between tables that will eventually enable you to easily provide the information the marketing team needs.**
    - Do this using LucidChart.
      - Go to [the Lucid app](https://lucid.app/documents#/dashboard)
      - Create a new document, based on the following template : `Database ER diagram (crow's foot)`. To do so, in the **Documents** section : Hit New > Lucidchart > Create from Template > Type "Database ER diagram (crow's foot)"
    - Export your LucidChart diagram and execute the SQL script in Postgres. Instructions are here : [Lucidchart Tutorials - Export your ERD](https://www.youtube.com/watch?v=q8hdO8Fqjcc&ab_channel=LucidSoftware)

2. [Optional - Not needed to answer the marketing team question] **❓There are several types of discounts : 1/ discounts on the order (20% off, 10% off, 50€ off) 2/ promo on a specific product (3.49€ instead of 3.99€). How would you reflect those in the DB structure ? (This could be added to the schema you started creating above)**

3. **❓ In pseudo code, write a SQL query that returns:**
    - `customer_id`
    - `first_name`
    - `last_name`
    - `email_address`
    - `num_orders` (total number of orders finalized by the customer)
    - `ltv` (lifetime value: total amount of money spent by the customer on the platform)
    - `most_frequently_purchased_product_name` (in terms of quantity purchased)

4. Optional: **❓ Another way of visualizing the ERD Diagram is to "code it" - using DBML (Database Markdown Language) - instead of "drawing" it with Lucidchart. Do the same thing you did in Question 1, but with [DBML](https://www.dbml.org/home/)
    - Your DBML file should include: all the tables, the columns they contain, as well as the type of those columns
    - If a column can only accept a certain set of values, document it somewhere
    - You should also document how tables link to each other (through which field)
    <details>
    <summary markdown='span'>Notes & resources 💡</summary>

      - [How to write a DBML file](https://www.dbml.org/docs/#table-alias)
      - [How to display a DBML file](https://www.dbml.org/home/#what-can-i-do-now)
      - Table names should be singular. There's no debate! (or if you want to be convinced, go check [this StackOverflow thread](https://stackoverflow.com/questions/338156/table-naming-dilemma-singular-vs-plural-names))

      Note that a well written DBML file can automatically generate the SQL code to build the tables listed in the DBML file.

    </details>

5. Optional: **❓ if you have time, feel free to actually build this database structure, and insert some fake data in it!**
