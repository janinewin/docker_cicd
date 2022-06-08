WITH purchase_attributes AS (
  SELECT 
      customer_id
    , COUNT(DISTINCT order_id) AS num_orders
    , SUM(total_spent)         AS ltv
  FROM order
  GROUP BY customer_id
)

, product_purchased AS (
  SELECT 
      O.customer_id 
    , P.product_name
    , SUM(quantity) AS total_quantity
  FROM order AS O 
  LEFT JOIN order_item AS OI 
    ON O.order_id = OI.order_id
  LEFT JOIN product AS P 
    ON OI.product_id = P.product_id 
  GROUP BY O.customer_id, P.product_name
)

, product_ranking AS (
  SELECT 
      customer_id
    , product_name 
    , ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY total_quantity DESC) AS ranking
  FROM product_purchased
)

, favorite_product AS (
  SELECT 
      customer_id
    , product_name
  FROM product_ranking
  WHERE ranking = 1
)

SELECT 
    C.customer_id
  , C.first_name
  , C.last_name
  , C.email_address
  , PA.num_orders
  , PA.ltv
  , FP.product_name AS favorite_product_name
FROM customer AS C 
  LEFT JOIN purchase_attributes AS PA
    ON C.customer_id = PA.customer_id
  LEFT JOIN favorite_product AS FP 
    ON C.customer_id = FP.customer_id
