SELECT
	r.id AS RepoID,
	r.name AS RepoName,
	r.programming_language,
	rv.name_of_vulnerability
FROM repo_vulnerabilities rv
JOIN repositories r ON r.id = rv.repository_id
WHERE rv.analysis_id = 17