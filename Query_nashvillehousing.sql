-- Showing data
SELECT * FROM Portfolio_DA..nashville_housing


-- Standardize date format
SELECT SaleDate, CONVERT(Date, SaleDate) FROM Portfolio_DA..nashville_housing

ALTER TABLE nashville_housing
ADD SaleDateConverted DATE;

UPDATE nashville_housing
SET SaleDateConverted = CONVERT(DATE, SaleDate)

SELECT SaleDateConverted FROM Portfolio_DA..nashville_housing


-- Fix address	
SELECT * FROM Portfolio_DA..nashville_housing
--WHERE PropertyAddress IS NULL

SELECT a.ParcelID, b.ParcelID, a.PropertyAddress, b.PropertyAddress, ISNULL(a.PropertyAddress, b.PropertyAddress)
FROM Portfolio_DA..nashville_housing a
JOIN Portfolio_DA..nashville_housing b
	ON a.ParcelID = b.ParcelID
	AND a.[UniqueID ] <> b.[UniqueID ]
--WHERE a.PropertyAddress IS NULL

UPDATE a
SET PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)
FROM Portfolio_DA..nashville_housing a
JOIN Portfolio_DA..nashville_housing b
	ON a.ParcelID = b.ParcelID
	AND a.[UniqueID ] <> b.[UniqueID ]
WHERE a.PropertyAddress IS NULL
