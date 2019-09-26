SELECT * FROM USERS_CREATE( 'admin@email.com', 'pbkdf2:sha256:150000$c30CjWVB$d1d6d544dfffd2dee5488cfe89cc2f965a8c4cddbf9180ad206f272237a5fa1a', 'Ima Admin', 'Ima Group', true);
SELECT * FROM USERS_CREATE('user@email.com', 'pbkdf2:sha256:150000$K5efuBwy$fcaa41a3203fd8f64b5d4aee241365ffa35e0a3a1c02f605bbc20cbea701cf89', 'Ima User', 'Ima Group' , true);
