SELECT
	A.date_id
	, A.year_of_calendar
	, A.month_of_year
	, A.day_of_month
	, A.day_of_week
	, A.hour_of_day
	, A.minute_of_day
	, B.tmax
	, CASE
		WHEN A.date_id = C.date_id THEN 1 ELSE 0 END AS holiday_ind
	, CAST(julianday(A.date_id) - julianday(C.date_id) AS INT) AS days_tofrom_holiday
	, ROUND(E.unemp_local - D.unemp_local,3) AS unemp_local_change
	, ROUND(E.unemp_natl - D.unemp_natl,3) AS unemp_natl_change
	, ROUND(E.cpi_natl - D.cpi_natl,3) AS cpi_natl_change
	, F.avg_wait_time_prev
	, A.wait_time
FROM
	T_WAIT_TIMES A
LEFT JOIN
	T_HI_TEMPERATURES B
	ON A.date_id = B.date_id
LEFT JOIN
	T_HOLIDAYS C
	ON ABS(julianday(A.date_id) - julianday(C.date_id)) <= 5
LEFT JOIN
	T_BLS_STATS D
	ON (
		(A.year_of_calendar = D.year_of_calendar AND A.month_of_year - D.month_of_year = 3) OR
		(A.year_of_calendar - D.year_of_calendar = 1 AND A.month_of_year - D.month_of_year = -9)
	)
LEFT JOIN
	T_BLS_STATS E
	ON (
		(A.year_of_calendar = E.year_of_calendar AND A.month_of_year - E.month_of_year = 4) OR
		(A.year_of_calendar - E.year_of_calendar = 1 AND A.month_of_year - E.month_of_year = -8)
	)
LEFT JOIN
	(SELECT
		 DATE(date_id, '+7 days') as date_id_match
		, hour_of_day
		, ROUND(AVG(wait_time),3) AS avg_wait_time_prev
	FROM
		T_WAIT_TIMES
	WHERE
		attraction_name='Soarin'
		AND wait_time >= 0
	GROUP BY
		DATE(date_id, '+7 days'), hour_of_day
		) F
	ON A.date_id = F.date_id_match
	AND A.hour_of_day = F.hour_of_day
WHERE
	A.attraction_name = 'Soarin'
	AND A.wait_time >= 0
	AND A.date_id >= '2015-01-08'
	AND A.date_id <= '2019-12-31';
