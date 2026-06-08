-- 1-5. Создание БД и таблиц
CREATE DATABASE IF NOT EXISTS Variant8_Work;
USE Variant8_Work;

-- Таблица Students
CREATE TABLE Students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    class_name VARCHAR(20) NOT NULL
);

-- Таблица Subjects
CREATE TABLE Subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(50) NOT NULL
);

-- Таблица teachers
CREATE TABLE teachers (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL
    );
	
-- Таблица TeacherSubjects
CREATE TABLE teachers_subjects (
    teacher_id INT,
    subject_id INT,
    PRIMARY KEY (teacher_id, subject_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

-- Таблица Grades
CREATE TABLE grades (
    grade_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    grade_value INT NOT NULL,
    grade_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

-- Таблица Attendance
CREATE TABLE attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- 6. Добавить 5 учеников
INSERT INTO students (full_name, class_name)
VALUES
('Сидоров Иван Сергеевич', '10А'),
('Петров Алексей Иванович', '10А'),
('Иванова Мария Владимировна', '10Б'),
('Кузнецов Дмитрий Александрович', '10Б'),
('Смирнова Анна Петровна', '10А');

-- 7. Добавить 3 предмета
INSERT INTO subjects (subject_name)
VALUES
('Математика'), 
('Русский язык'),
('Информатика');

-- 8. Добавить 2 учителя
INSERT INTO teachers (full_name)
VALUES
('Орлова Наталья Денисовна'),
('Васильев Сергей Артёмович');

-- 9. Связать учителей с предметами
INSERT INTO teachers_subjects
VALUES
(1, 1),
(1, 2),
(2, 3);
 
 -- 10. Добавить 10 оценок
 INSERT INTO grades
 (student_id, subject_id, grade_value, grade_date)
 VALUES
 (1,1,5,'2025-01-10'),
 (1,2,4,'2025-01-11'),
 (2,1,3,'2025-01-12'),
 (2,3,5,'2025-01-13'),
 (3,2,4,'2025-01-14'),
 (3,3,2,'2025-01-15'),
 (4,1,3,'2025-01-16'),
 (4,2,5,'2025-01-17'),
 (5,3,4,'2025-01-18'),
 (5,1,5,'2025-01-19');
 
 -- 11. Проставить посещаемость 
 INSERT INTO attendance
 (student_id, attendance_date, status)
 VALUES
 (1,'2025-01-10','Присутствовал'),
 (2,'2025-01-10','Отсутствовал'),
 (3,'2025-01-10','Присутствовал'),
 (4,'2025-01-10','Отсутствовал'),
 (5,'2025-01-10','Присутствовал'),
 (2,'2025-01-11','Отсутствовал'),
 (4,'2025-01-11','Присутствовал'),
 (2,'2025-01-12','Отсутствовал');
 
 -- 12. Вывести средний балл ученика 'Сидоров'
SELECT 
    s.full_name,
    AVG(g.grade_value) AS average_grade
FROM students s 
JOIN grades g 
ON s.student_id = g.student_id
WHERE s.full_name LIKE 'Сидоров%'
GROUP BY s.full_name;

-- 13.Вывести всех учеников, у которых есть хотя бы одна оценка 5
SELECT DISTINCT 
    s.full_name AS 'Ученик',
    s.class_name AS 'Класс'
FROM students s
JOIN grades g ON s.student_id = g.student_id
WHERE g.grade_value = 5
ORDER BY s.full_name;

-- 14. Ученики, отсортированные по среднему баллу (убывание)
SELECT 
    s.full_name AS 'Ученик',
    ROUND(IFNULL(AVG(g.grade_value), 0), 2) AS 'Средний балл'
FROM students s
LEFT JOIN grades g ON s.student_id = g.student_id
GROUP BY s.student_id
ORDER BY AVG(g.grade_value) DESC;

-- 15. Предметы и количество оценок по ним
SELECT 
    sub.subject_name AS 'Предмет',
    COUNT(g.grade_id) AS 'Количество оценок'
FROM subjects sub
LEFT JOIN grades g ON sub.subject_id = g.subject_id
GROUP BY sub.subject_id
ORDER BY COUNT(g.grade_id) DESC;

-- 16. Предметы, по которым средний балл ниже 3.5
SELECT 
    sub.subject_name AS 'Предмет',
    ROUND(AVG(g.grade_value), 2) AS 'Средний балл'
FROM subjects sub
JOIN grades g ON sub.subject_id = g.subject_id
GROUP BY sub.subject_id
HAVING AVG(g.grade_value) < 4;

-- 17. Дни, когда посещаемость была ниже 80%
SELECT 
    attendance_date AS 'Дата',
    ROUND(SUM(CASE WHEN status = 'Присутствовал' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS 'Процент посещаемости'
FROM attendance
GROUP BY attendance_date
HAVING (SUM(CASE WHEN status = 'Присутствовал' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) < 80;

-- 18. Ученики, у которых больше 2 пропусков
SELECT 
    s.full_name AS 'Ученик',
    COUNT(a.attendance_id) AS 'Количество пропусков'
FROM students s
JOIN attendance a ON s.student_id = a.student_id
WHERE a.status = 'Отсутствовал'
GROUP BY s.student_id
HAVING COUNT(a.attendance_id) > 2;

-- 19. Оценки, сгруппированные по месяцам
SELECT 
    DATE_FORMAT(grade_date, '%Y-%m') AS 'Месяц',
    COUNT(*) AS 'Количество оценок'
FROM grades
GROUP BY DATE_FORMAT(grade_date, '%Y-%m')
ORDER BY `Месяц`;

-- 20. Ученики, которые не получали оценок по информатике
SELECT 
    s.full_name AS 'Ученик',
    s.class_name AS 'Класс'
FROM students s
WHERE NOT EXISTS (
    SELECT 1 
    FROM grades g
    JOIN subjects sub ON g.subject_id = sub.subject_id
    WHERE g.student_id = s.student_id AND sub.subject_name = 'Информатика'
);

-- 21. Увеличить баллы всех оценок по математике на 1 (но не выше 5)
UPDATE grades g
JOIN subjects sub ON g.subject_id = sub.subject_id
SET g.grade_value = LEAST(g.grade_value + 1, 5)
WHERE sub.subject_name = 'Математика';

-- 22. Удалить оценки, у которых дата старше '2025-01-01'
DELETE FROM grades WHERE grade_date < '2025-01-01'; 

-- 23.  Добавить столбец email в Students
ALTER TABLE students ADD COLUMN email VARCHAR(100);

UPDATE students SET email = CONCAT(LOWER(REPLACE(full_name, ' ', '.')), '@school.ru');

-- 24. Создать представление StudentProgress
CREATE OR REPLACE VIEW StudentProgress AS
SELECT 
    s.student_id,
    s.full_name AS 'Ученик',
    sub.subject_name AS 'Предмет',
    ROUND(IFNULL(AVG(g.grade_value), 0), 2) AS 'Средний балл'
FROM students s
CROSS JOIN subjects sub
LEFT JOIN grades g ON s.student_id = g.student_id AND sub.subject_id = g.subject_id
GROUP BY s.student_id, sub.subject_id;

-- 25. Сложный запрос: для каждого учителя вывести предметы, средний балл, процент посещаемости
SELECT 
    t.full_name AS 'Учитель',
    sub.subject_name AS 'Предмет',
    ROUND(IFNULL(AVG(g.grade_value), 0), 2) AS 'Средний балл',
    CONCAT(
        ROUND(
            IFNULL(
                SUM(CASE WHEN a.status = 'Присутствовал' THEN 1 ELSE 0 END) * 100.0 / 
                NULLIF(COUNT(DISTINCT CONCAT(a.student_id, a.attendance_date)), 0), 
                0
            ), 
            2
        ), '%'
    ) AS 'Процент посещаемости'
FROM teachers t
JOIN teachers_subjects ts ON t.teacher_id = ts.teacher_id
JOIN subjects sub ON ts.subject_id = sub.subject_id
LEFT JOIN grades g ON sub.subject_id = g.subject_id
LEFT JOIN attendance a ON g.student_id = a.student_id AND g.grade_date = a.attendance_date
GROUP BY t.teacher_id, sub.subject_id
ORDER BY t.full_name, sub.subject_name;