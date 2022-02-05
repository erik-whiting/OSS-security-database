SELECT topic, COUNT(*) AS occurences
FROM repo_topics
GROUP BY topic
ORDER BY occurences DESC;