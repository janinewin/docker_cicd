## [DEPRECATED]

This should be deprecated for now
Because the `ratings` table logs ratings with values between 1 and 5
While the averages observed in the `movies_metadata` table have a range between 1 and 10


## Goal of this section

The previous exercice was very guided. Though both data engineers or data analyst usually deal with vague requests. This section tests your ability to decompose a high level question into sub questions, that translate into concrete SQL queries which the output will provide some elements of answers

## Exercices

1. The `ratings` table seems to log all the ratings left by all the users over time. Before deep diving into this table, as a data engineer, you would like to check the consistency of this table : hence verifying that when recomputing the average rating from this table, you match the average rating recorded - for each movie - in the `movies_metadata` table. How would you do that ? 

