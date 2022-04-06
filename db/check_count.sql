SELECT SUM(TimesDetected) FROM (
	SELECT
		r.id AS RepoID,
		r.name AS RepoName,
		r.programming_language,
		rv.name_of_vulnerability AS Vulnerability,
		COUNT(rv.name_of_vulnerability) AS TimesDetected
	FROM repo_vulnerabilities rv
	JOIN repositories r ON r.id = rv.repository_id
	WHERE rv.analysis_id = 17
	GROUP BY r.id, rv.name_of_vulnerability
) AS sub

-- The result of this should equal the same as the results of
-- SELECT COUNT(*) FROM repo_vulnerabilities