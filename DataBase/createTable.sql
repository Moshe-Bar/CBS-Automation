REM   Script: level0
REM   schema of Line, Station, Ride, Bus, Driver and stops

CREATE TABLE Line ( 
    Line_Number    NUMBER(3) NOT NULL, 
    source         VARCHAR(50) NOT NULL, 
    dest           VARCHAR(50) NOT NULL, 
CONSTRAINT pk_Line PRIMARY KEY (Line_Number));

CREATE TABLE Station ( 
    location       VARCHAR(20) NOT NULL, 
    Station_number NUMBER(5) NOT NULL, 
CONSTRAINT pk_Station PRIMARY KEY (Station_number));

CREATE TABLE ride ( 
    start_time     TIMESTAMP(1) NOT NULL, 
    finish_time    TIMESTAMP(1) NOT NULL, 
    Line_Number    NUMBER(3) NOT NULL, 
CONSTRAINT pk_ride PRIMARY KEY (start_time,finish_time,Line_Number), 
CONSTRAINT fk_ride FOREIGN KEY (Line_Number) 
    REFERENCES Line (Line_Number) 
    ON DELETE CASCADE);

CREATE TABLE Stops (
    Station_number NUMBER(5) NOT NULL,
    Line_Number    NUMBER(3) NOT NULL,
    isSource         CHAR(1) CHECK(isSource in ('Y','N')),
    isDest           CHAR(1) CHECK(isDest in ('Y','N')),
CONSTRAINT pk_Stops PRIMARY KEY (Station_number,Line_Number),
CONSTRAINT fk_Stops FOREIGN KEY (Station_number)
    REFERENCES Station (Station_number)
    ON DELETE CASCADE,
CONSTRAINT fk_Stops2 FOREIGN KEY (Line_Number)
    REFERENCES Line (Line_Number)
    ON DELETE CASCADE);


CREATE TABLE Bus (
    license_plate   NUMBER(8) NOT NULL,
    Line_Number    NUMBER(3) NOT NULL,
CONSTRAINT pk_Bus PRIMARY KEY (license_plate ),
CONSTRAINT fk_Bus FOREIGN KEY (Line_Number)
    REFERENCES Line (Line_Number));


CREATE TABLE Driver (
    Id             NUMBER(9) NOT NULL,
    License_number NUMBER(7) NOT NULL,
    Name           VARCHAR(20) NOT NULL,
    Salary         NUMBER(10) NOT NULL,
    license_plate NUMBER(8) NOT NULL,
CONSTRAINT pk_Driver PRIMARY KEY (Id),
CONSTRAINT fk_Driver FOREIGN KEY (license_plate)
    REFERENCES Bus (license_plate));


