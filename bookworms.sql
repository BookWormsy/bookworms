CREATE TABLE HasBadge
(
 idBadge int NOT NULL ,
 idUser  int NOT NULL ,

PRIMARY KEY (idBadge, idUser),
KEY FK_1 (idBadge),
CONSTRAINT FK_10 FOREIGN KEY FK_1 (idBadge) REFERENCES Badge (idBadge),
KEY FK_2 (idUser),
CONSTRAINT FK_11 FOREIGN KEY FK_2 (idUser) REFERENCES UsernamesPasswords (idUser)
);

CREATE TABLE RecommendationList
(
 idUser int NOT NULL ,
 idBook int NOT NULL ,

PRIMARY KEY (idUser, idBook),
KEY FK_1 (idUser),
CONSTRAINT FK_18 FOREIGN KEY FK_1 (idUser) REFERENCES UsernamesPasswords (idUser),
KEY FK_2 (idBook),
CONSTRAINT FK_19 FOREIGN KEY FK_2 (idBook) REFERENCES Book (idBook)
);