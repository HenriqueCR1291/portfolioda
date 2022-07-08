-- Joining the tables
WITH hotels AS (
SELECT * FROM Portfolio_DA..['2018$']
UNION
SELECT * FROM Portfolio_DA..['2019$']
UNION
SELECT * FROM Portfolio_DA..['2020$']
)
SELECT * FROM hotels


-- Converting timestamp to date format and showing check out dates
WITH hotels AS (
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2018$']
UNION
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2019$']
UNION
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2020$']
)
SELECT MIN(reservation_status_date_upd) AS min_, MAX(reservation_status_date_upd) AS max_ FROM hotels
GROUP BY arrival_date_year


-- Selecting different date
WITH hotels AS (
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2018$']
UNION
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2019$']
UNION
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2020$']
)
SELECT * FROM hotels
WHERE reservation_status_date_upd = '2014-10-17' AND arrival_date_year = '2019'


-- Showing different types of deposit and reservation
WITH hotels AS (
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2018$']
UNION
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2019$']
UNION
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2020$']
)
SELECT DISTINCT deposit_type, reservation_status FROM hotels


-- Showing what is Non refund and refundable types
WITH hotels AS (
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2018$']
UNION
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2019$']
UNION
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2020$']
)
SELECT * FROM hotels
WHERE deposit_type = 'Non Refund' OR deposit_type = 'Refundable'


-- Calculating how much made per year
WITH hotels AS (
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2018$']
UNION
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2019$']
UNION
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2020$']
)
SELECT arrival_date_year, hotel, deposit_type, SUM((stays_in_weekend_nights+stays_in_week_nights)*adr) AS revenue FROM hotels
WHERE deposit_type != 'No Deposit'
GROUP BY arrival_date_year, hotel, deposit_type


-- Joinning meals and market tables
WITH hotels AS (
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2018$']
UNION
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2019$']
UNION
SELECT *, CAST(reservation_status_date AS DATE) AS reservation_status_date_upd FROM Portfolio_DA..['2020$']
)
SELECT * FROM hotels
LEFT JOIN Portfolio_DA..market_segment$
ON hotels.market_segment = market_segment$.market_segment
LEFT JOIN Portfolio_DA..meal_cost$
ON meal_cost$.meal = hotels.meal
