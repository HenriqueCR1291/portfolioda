SELECT * FROM Portfolio_DA..covid_deaths
ORDER BY 3,4

SELECT * FROM Portfolio_DA..covid_vaccinations
ORDER BY 3,4


-- Filtering
SELECT location,date, total_cases, new_cases, total_deaths, population
FROM Portfolio_DA..covid_deaths
ORDER BY 1,2


-- Total cases per total deaths
SELECT location,date, total_cases, total_deaths, (total_deaths/total_cases)*100 AS death_percentage
FROM Portfolio_DA..covid_deaths
WHERE location like '%sweden'
ORDER BY 1,2


-- Total cases per population
SELECT location,date, total_cases, population, (total_cases/population)*100 AS cases_percentage
FROM Portfolio_DA..covid_deaths
WHERE location like '%sweden'
ORDER BY 1,2


-- Countries with highest infection count
SELECT location,population, MAX(total_cases) AS highestinfectioncount, MAX((total_cases/population))*100 AS percent_population_infected
FROM Portfolio_DA..covid_deaths
--WHERE location like '%sweden'
GROUP BY location,	population
ORDER BY 4 DESC


-- Countries with highest death count
SELECT location, MAX(CAST(total_deaths as int)) AS totaldeathcount
FROM Portfolio_DA..covid_deaths
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY 2 DESC


-- Continents with highest death count
SELECT location, MAX(CAST(total_deaths as int)) AS totaldeathcount
FROM Portfolio_DA..covid_deaths
WHERE continent IS NULL
GROUP BY location
ORDER BY 2 DESC

SELECT continent, MAX(CAST(total_deaths as int)) AS totaldeathcount
FROM Portfolio_DA..covid_deaths
WHERE continent IS not NULL
GROUP BY continent
ORDER BY 2 DESC


-- 1) Global count
SELECT SUM(new_cases) AS total_cases, SUM(CAST(new_deaths as int)) AS total_deaths, SUM(CAST(new_deaths as int))/SUM(new_cases)*100 AS death_percentage
FROM Portfolio_DA..covid_deaths
WHERE continent IS NOT NULL
ORDER BY 1,2


-- 2) Total death
SELECT location, SUM(CAST(new_deaths as int)) AS total_death_count
FROM Portfolio_DA..covid_deaths
WHERE continent IS NULL AND location NOT IN ('World', 'Upper middle income', 'High Income', 'Lower middle income', 'European Union', 'Low income', 'International')
GROUP BY location
ORDER BY total_death_count DESC


-- 3) Countries with highest infection count
SELECT location,population, MAX(total_cases) AS highest_infection_count, MAX((total_cases/population))*100 AS percent_population_infected
FROM Portfolio_DA..covid_deaths
WHERE location like '%sweden'
GROUP BY location,	population
ORder by 3


-- 4) Countries with highest infection count
SELECT location,population, date, MAX(total_cases) AS highest_infection_count, MAX((total_cases/population))*100 AS percent_population_infected
FROM Portfolio_DA..covid_deaths
--WHERE location like '%sweden'
GROUP BY location,	population, date
ORder by 3


--Total population vs vaccinations using CTE
WITH PopvsVac (continent, location, date, population, new_vaccinations, RollingPeopleVaccinated)
as
(
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CONVERT(bigint, vac.new_vaccinations)) OVER(PARTITION BY dea.location order by dea.location, dea.date) as rolling_people_vaccinated
FROM Portfolio_DA..covid_deaths dea
JOIN Portfolio_DA..covid_vaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL AND dea.location like '%brazil'
--ORDER BY 2,3
)
SELECT *, (RollingPeopleVaccinated/population)*100
FROM PopvsVac


--Total population vs vaccinations using temp table
DROP TABLE IF EXISTS #PercentPopulationVaccinated
CREATE TABLE #PercentPopulationVaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric,
new_vaccinations numeric,
RollingPeopleVaccinated numeric
)

INSERT INTO #PercentPopulationVaccinated
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CONVERT(bigint, vac.new_vaccinations)) OVER(PARTITION BY dea.location order by dea.location, dea.date) as rolling_people_vaccinated
FROM Portfolio_DA..covid_deaths dea
JOIN Portfolio_DA..covid_vaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL AND dea.location like '%brazil'
--ORDER BY 2,3

SELECT *, (RollingPeopleVaccinated/population)*100
FROM #PercentPopulationVaccinated


-- Creating view
CREATE VIEW PercentPopulationVaccinated as
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CONVERT(bigint, vac.new_vaccinations)) OVER(PARTITION BY dea.location order by dea.location, dea.date) as rolling_people_vaccinated
FROM Portfolio_DA..covid_deaths dea
JOIN Portfolio_DA..covid_vaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL

SELECT * FROM PercentPopulationVaccinated