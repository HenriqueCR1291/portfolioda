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


--Breaking address in address, city
SELECT PropertyAddress FROM Portfolio_DA..nashville_housing

SELECT SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)-1) AS Address,
SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress)+1, LEN(PropertyAddress)) AS City FROM Portfolio_DA..nashville_housing

ALTER TABLE Portfolio_DA..nashville_housing
ADD PropertySplitAddress Nvarchar(255)

UPDATE Portfolio_DA..nashville_housing
SET PropertySplitAddress = SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)-1)

ALTER TABLE Portfolio_DA..nashville_housing
ADD PropertySplitCity Nvarchar(255)

UPDATE Portfolio_DA..nashville_housing
SET PropertySplitCity = SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress)+1, LEN(PropertyAddress))


SELECT PARSENAME(REPLACE(OwnerAddress, ',','.'), 3),
PARSENAME(REPLACE(OwnerAddress, ',','.'), 2),
PARSENAME(REPLACE(OwnerAddress, ',','.'), 1)
FROM Portfolio_DA..nashville_housing

ALTER TABLE Portfolio_DA..nashville_housing
ADD OwnerSplitAddress Nvarchar(255)

UPDATE Portfolio_DA..nashville_housing
SET OwnerSplitAddress = PARSENAME(REPLACE(OwnerAddress, ',','.'), 3)

ALTER TABLE Portfolio_DA..nashville_housing
ADD CitySplitAddress Nvarchar(255)

UPDATE Portfolio_DA..nashville_housing
SET CitySplitAddress = PARSENAME(REPLACE(OwnerAddress, ',','.'), 2)

ALTER TABLE Portfolio_DA..nashville_housing
ADD StateSplitAddress Nvarchar(255)

UPDATE Portfolio_DA..nashville_housing
SET StateSplitAddress = PARSENAME(REPLACE(OwnerAddress, ',','.'), 1)

SELECT * FROM Portfolio_DA..nashville_housing


-- SoldasVacant
SELECT DISTINCT(SoldAsVacant), COUNT(SoldAsVacant) 
FROM Portfolio_DA..nashville_housing
GROUP BY SoldAsVacant
ORDER BY 2 DESC

SELECT SoldAsVacant,
CASE WHEN SoldAsVacant = 'Y' THEN 'Yes'
	 WHEN SoldAsVacant = 'N' THEN 'No'
	 ELSE SoldAsVacant
	 END
FROM Portfolio_DA..nashville_housing

UPDATE Portfolio_DA..nashville_housing
SET SoldAsVacant = CASE WHEN SoldAsVacant = 'Y' THEN 'Yes'
	 WHEN SoldAsVacant = 'N' THEN 'No'
	 ELSE SoldAsVacant
	 END