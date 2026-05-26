-- Top hours with highest average temperature in Bangalore
SELECT
  hour,
  ROUND(AVG(temperature_c), 2) AS avg_temp_celsius,
  ROUND(AVG(humidity_percent), 2) AS avg_humidity,
  COUNTIF(feels_hot = TRUE) AS hot_hours_count
FROM `tacheon-assessment-497521.weather_data.hourly_weather`
GROUP BY hour
ORDER BY avg_temp_celsius DESC
LIMIT 10;
