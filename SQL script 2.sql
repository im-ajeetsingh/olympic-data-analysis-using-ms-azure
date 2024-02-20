SELECT *from teams;
--Count the no. of Athletes from each country:
SELECT Country, count(*) as TotalAthletes
from athletes
group by Country
order by TotalAthletes DESC;

--Calculate the total no of Medal by each country

SELECT 
Team_Country,
sum(Gold) as Total_Gold,
sum(Silver) as Total_Silver,
sum(Bronze) as Total_Bronze
from medals
group by Team_Country
ORDER by Total_Gold desc;

--Calculate the average number of gender for each discipline:
select Discipline,
AVG(Female) Avg_Female,
AVG(Male) Avg_Male
FROM entriesgender
group by Discipline;