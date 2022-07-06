
{{
  config(
    materialized='view'
  )
}}

WITH users_summary AS (
SELECT
    author

  , {{ num_types('comment') }}
  , {{ first_type_at('comment') }}
  , {{ last_type_at('comment') }}

  , {{ num_types('story') }}
  , {{ first_type_at('story') }}
  , {{ last_type_at('story') }}

FROM {{ ref('stg_hackernews_full' )}}
GROUP BY 1
)

SELECT
    author                                            AS user_id
  , CONCAT(
      'https://news.ycombinator.com/user?id='
      , author)                                       AS user_url
  , IFNULL(num_comment, 0)                            AS num_comment
  , first_comment_at                                  AS first_comment_at
  , last_comment_at                                   AS last_comment_at

  , IFNULL(num_story, 0)                              AS num_story
  , first_story_at                                    AS first_story_at
  , last_story_at                                     AS last_story_at

FROM users_summary
