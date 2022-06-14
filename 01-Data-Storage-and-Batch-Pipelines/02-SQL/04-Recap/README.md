## Goal of this section

As a data engineer, you need to be able to think of a data structure (tables, columns etc) in your data warehouse that's 
- not repetitive (similar information is not repetited in many fields or tables)
- easy to read, understand and manipulate for data analysts or scientists

Hence, from a very raw and disorganized data extracted from the different systems your company interacts with, the data engineer needs to write scripts to map this unstructured data into a clean and limited set of tables : this is called "Data Modeling". And it's now becoming a full time data position in tech companies, called "Analytics Engineer".

The exercice is split into 2 parts : 
- A high level business question
- An underlying design question

You have to think of a data structure that would be optimized for the business, and would enable the data analyst to, in a simple query on top of those tables, answer the business question that is asked. 

Hence there will be 2 deliverables : 
- a DBML / ERD Diagram that shows the structure of tables the student has in mind
- the SQL query to answer the business question

## Exercices

You work in Company ABC, which sells products online. The marketing team would like to, everyday, push to their CRM the list of all their customers, with their first name, last name, and email address, with some attributes related to their behavior. So that they can efficiently target them.

Note that orders can be either "completed", or "canceled".

1. Provide the underlying minimalistic database structure and relationships between tables (in a dmbl format) that enables you to easily write this SQL query. 
  - You DBML file should include : all the tables, the columns they contain, as well as the type of those columns
  - If a column can only accept a certain set of values, document it somewhere
  - You should also document how tables link to each other (through which field)

Content + Notes : 
  - [How to write a DBML file](https://www.dbml.org/docs/#table-alias)
  - [How to display a DBML file](https://www.dbml.org/home/#what-can-i-do-now)
  - Table names should be singular. There's no debate ! (or if you want to be convinced, go check [this StackOverflow thread](https://stackoverflow.com/questions/338156/table-naming-dilemma-singular-vs-plural-names)) 

Note that a well written DBML file can automatically generate the SQL code to build the tables listed in the DBML file

2. In pseudo code (or if you have time, feel free to actually build this database structure, and insert some fake data in it), could you write a SQL query that returns : 
- `customer_id` 
- `first_name` 
- `last_name`
- `email_address`
- `num_orders` (total number of orders finalized by the customer)
- `ltv` (lifetime value : total amount of money spent by the customer on the platform)
- `most_frequently_purchased_product_name` (in terms of quantity purchased)

