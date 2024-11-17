DROP TABLE IF EXISTS user_answer;
DROP TABLE IF EXISTS optional_answer;
DROP TABLE IF EXISTS question;

CREATE TABLE question (
    question_id INT(11) NOT NULL AUTO_INCREMENT,
    title VARCHAR(300) NOT NULL,
    PRIMARY KEY (question_id)
);

CREATE TABLE optional_answer (
    answer_id INT(11) NOT NULL AUTO_INCREMENT,
    question_id INT(11) NOT NULL,
    optional_answer_text VARCHAR(300) NOT NULL,
    PRIMARY KEY (answer_id),
    FOREIGN KEY (question_id) REFERENCES question(question_id)
);


CREATE TABLE user_answer (
    id INT(11) NOT NULL AUTO_INCREMENT,
    answer_id INT(11) NOT NULL,
    user_id INT(11) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (answer_id) REFERENCES optional_answer(answer_id)
);