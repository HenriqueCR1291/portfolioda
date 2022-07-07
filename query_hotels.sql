
WITH hotels AS (
SELECT * FROM Portfolio_DA..['2018$']
UNION
SELECT * FROM Portfolio_DA..['2019$']
UNION
SELECT * FROM Portfolio_DA..['2020$']
)
SELECT * FROM hotels