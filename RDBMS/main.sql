-- 1
SELECT ID, name, max(salary) salary FROM instructor ORDER by name;

-- 2
SELECT ID, name, dept_name, min(salary) salary FROM instructor GROUP by dept_name ORDER by name;

-- 3
SELECT ID, name, building FROM instructor NATURAL JOIN department WHERE building != "Painter" ORDER by name;

-- 4
SELECT * FROM
(SELECT i.ID, i.name, c.course_id, c.title
FROM instructor i JOIN course c, teaches t
WHERE t.course_id = c.course_id and i.ID = t.ID)
GROUP by ID  HAVING count(course_id)=1 ORDER by name;

-- 5
SELECT ID, name, 100-count(course_id) num_courses  FROM
(SELECT i.ID, i.name, t.course_id
FROM instructor i, teaches t 
WHERE i.ID != t.ID)
GROUP by ID ORDER by ID;

-- 6
SELECT * FROM
(SELECT course_id, title, count(prereq_id) num_prereq FROM
(SELECT c.course_id, c.title, p.prereq_id FROM course c, prereq p
WHERE c.course_id=p.course_id)
GROUP by course_id)
WHERE num_prereq>1 ORDER by course_id;

-- 7
SELECT * FROM
(SELECT prereq_id, title, count(course_id) prereq_for FROM
(SELECT p.prereq_id, c.title, p.course_id FROM prereq p, course c
WHERE p.prereq_id=c.course_id)
GROUP by prereq_id)
WHERE prereq_for >1
ORDER by prereq_id;

-- 8
SELECT ID, name FROM
(SELECT ID, name, 30000-count(course_id) not_reg_any FROM
(SELECT s.ID, s.name, t.course_id FROM student s, takes t
WHERE s.ID != t.ID)
GROUP by ID)
WHERE not_reg_any=0;

-- 9
SELECT ID, name, 30000-count(course_id) num_courses FROM
(SELECT s.ID, s.name, t.course_id FROM student s, takes t
WHERE s.ID != t.ID)
GROUP by ID;

-- 10
CREATE VIEW temp1 as
SELECT s.ID, s.name, t.course_id, c.title, t.semester, t.year
FROM student s, takes t, course c
WHERE s.ID = t.ID AND t.course_id = c.course_id;

CREATE VIEW temp2 as
SELECT t1.ID, t1.name, t1.course_id, t1.title, t1.semester, t1.year
FROM temp1 t1, temp1 t2
WHERE t1.ID = t2.ID AND t1.course_id = t2.course_id AND NOT(t1.semester = t2.semester AND t1.year=t2.year)
ORDER by t1.ID;
 
CREATE VIEW maxy as SELECT ID, course_id,max(year) year FROM temp2 GROUP by ID, course_id;


SELECT table1.ID, table1.name, table1.course_id, table1.title, table1.recent_sem, table1.recent_year, table2.num_times
FROM
(SELECT t1.ID, t1.name, t1.course_id, t1.title, t1.semester recent_sem, t1.year recent_year
FROM temp2 t1, temp2 t2, maxy m
WHERE t1.ID = t2.ID AND t1.ID = m.ID AND t2.ID = m.ID AND
t1.course_id = t2.course_id AND t1.course_id = m.course_id AND t2.course_id = m.course_id
AND t1.year = m.year AND t1.year = t2.year AND t1.semester <= t2.semester
EXCEPT
SELECT t1.ID, t1.name, t1.course_id, t1.title, t1.semester recent_sem, t1.year recent_year
FROM temp2 t1, temp2 t2, maxy m
WHERE t1.ID = t2.ID AND t1.ID = m.ID AND t2.ID = m.ID AND
t1.course_id = t2.course_id AND t1.course_id = m.course_id AND t2.course_id = m.course_id
AND t1.year = m.year AND t1.year = t2.year AND t1.semester > t2.semester) as table1
LEFT JOIN
(SELECT DISTINCT ID, course_id, count(course_id) num_times
FROM (SELECT DISTINCT * FROM temp2)
GROUP by ID, course_id
ORDER by ID) as table2
ON table1.ID = table2.ID AND table1.course_id = table2.course_id
ORDER BY table1.ID;