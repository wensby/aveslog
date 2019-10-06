SELECT
  id,
  person_id,
  bird_id,
  sighting_date,
  sighting_time
FROM sighting
WHERE person_id = %s
ORDER BY
  sighting_date DESC,
  sighting_time DESC;
