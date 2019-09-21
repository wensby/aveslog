SELECT
  s.id AS sighting_id,
  b.id AS bird_id,
  b.binomial_name AS bird_name,
  s.sighting_date AS sighting_date,
  s.sighting_time AS sighting_time,
  p.filepath AS thumbnail_filepath
FROM sighting AS s
LEFT JOIN bird AS b ON s.bird_id = b.id
LEFT JOIN bird_thumbnail AS bt ON b.id = bt.bird_id
LEFT JOIN picture AS p ON p.id = bt.picture_id
WHERE s.person_id = %s
ORDER BY
  s.sighting_date DESC,
  s.sighting_time DESC;