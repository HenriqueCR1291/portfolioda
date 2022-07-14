/****** Script do comando SelectTopNRows de SSMS  ******/
SELECT * FROM [Portfolio_DA].[dbo].[nashville_housing]
--Subquery
SELECT UniqueID, TotalValue, (SELECT AVG(TotalValue) FROM [Portfolio_DA].[dbo].[nashville_housing]) AS ValueAVG FROM [Portfolio_DA].[dbo].[nashville_housing]


--Partition by
SELECT UniqueID, TotalValue, AVG(TotalValue) OVER() AS ValueAVG FROM [Portfolio_DA].[dbo].[nashville_housing]


--Group by
SELECT UniqueID, TotalValue, AVG(TotalValue) AS ValueAVG FROM [Portfolio_DA].[dbo].[nashville_housing]
GROUP BY UniqueID, TotalValue


--Subquery in from
SELECT a.UniqueID, ValueAVG
FROM (SELECT UniqueID, TotalValue, AVG(TotalValue) OVER() AS ValueAVG FROM [Portfolio_DA].[dbo].[nashville_housing]) a


--Subquery in where
SELECT UniqueID, TotalValue FROM [Portfolio_DA].[dbo].[nashville_housing]
WHERE UniqueID in (SELECT UniqueID FROM [Portfolio_DA].[dbo].[nashville_housing] WHERE LandUse = 'SINGLE FAMILY')


--Create temp table
CREATE TABLE #staff(
EmployeeID int,
Jobtitle VARCHAR(100),
Salary int)

INSERT INTO #staff VALUES(
'001', 'Analyst', '10000'),(
'002', 'Specialist', '20000')

SELECT * FROM #staff

--Create a normal table
CREATE TABLE staff2(
EmployeeID int,
Jobtitle VARCHAR(100),
Salary int)

INSERT INTO staff2 VALUES(
'003', 'Analyst', '50000'),(
'004', 'Specialist', '25000')

SELECT * FROM staff2

--Populate values from normal table into temp table
INSERT INTO #staff
SELECT * FROM staff2

SELECT * FROM #staff
