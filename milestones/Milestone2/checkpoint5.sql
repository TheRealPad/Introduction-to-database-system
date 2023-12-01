USE HealthManagementSystemDB;

DROP FUNCTION IF EXISTS getOrCreateLanguageId;
DROP FUNCTION IF EXISTS getOrCreateRegionId;
DROP FUNCTION IF EXISTS getOrCreateOSId;
DROP FUNCTION IF EXISTS getBiggestEvent;

DROP TRIGGER IF EXISTS CREATE_SOCIAL_SECURITY_NUMBER;
DROP TRIGGER IF EXISTS DELETE_USER_ACCOUNT;

DROP PROCEDURE IF EXISTS GetUserEmailsByRegion;

DELIMITER $$

CREATE FUNCTION getOrCreateLanguageId(languageCode VARCHAR(45), languageName VARCHAR(255))
    RETURNS INT
BEGIN
    DECLARE languageId INT;
    
    SELECT language_id INTO languageId
    FROM Language
    WHERE name = languageName;
    IF languageId IS NULL THEN
        SELECT language_id INTO languageId
        FROM Language
        WHERE code = languageCode;
        IF languageId IS NULL THEN
            INSERT INTO Language (code, name)
            VALUES (languageCode, languageName);
            SELECT LAST_INSERT_ID() INTO languageId;
        END IF;
    END IF;
    RETURN languageId;
END $$

    
    CREATE FUNCTION getOrCreateRegionId(regionCode VARCHAR(45), regionName VARCHAR(255))
	RETURNS INT
	BEGIN
		DECLARE regionId INT;

		SELECT region_id INTO regionId
		FROM Region
		WHERE name = regionName;
		IF regionId IS NULL THEN
			SELECT region_id INTO regionId
			FROM Region
			WHERE code_area = regionCode;
			IF regionId IS NULL THEN
				INSERT INTO Region (code_area, name)
				VALUES (regionCode, regionName);
				SELECT LAST_INSERT_ID() INTO regionId;
			END IF;
		END IF;
		RETURN regionId;
	END $$
    
    CREATE FUNCTION getOrCreateOSId(osCode VARCHAR(45), osName VARCHAR(255))
	RETURNS INT
	BEGIN
		DECLARE osId INT;
        
		SELECT os_id INTO osId
		FROM OS
		WHERE name = osName;
		IF osId IS NULL THEN
			SELECT os_id INTO osId
			FROM OS
			WHERE code = osCode;
			IF osId IS NULL THEN
				INSERT INTO OS (code, name)
				VALUES (osCode, osName);
				SELECT LAST_INSERT_ID() INTO osId;
			END IF;
		END IF;
		RETURN osId;
	END $$
    
    CREATE TRIGGER CREATE_SOCIAL_SECURITY_NUMBER AFTER INSERT ON User 
	FOR EACH ROW 
	BEGIN 
		INSERT INTO SocialNumber (value, user) 
		VALUES (NEW.email, NEW.user_id);
	END$$
    
    CREATE TRIGGER DELETE_USER_ACCOUNT BEFORE DELETE ON User 
	FOR EACH ROW 
	BEGIN 
		DELETE FROM Account WHERE user_id = OLD.user_id;
	END$$
    
    CREATE PROCEDURE GetUserEmailsByRegion(IN regionCode VARCHAR(45))
	BEGIN
		SELECT u.email
		FROM Account a
		JOIN User u ON u.user_id = a.user_id
		WHERE a.region = (SELECT region_id FROM Region r WHERE r.code_area = regionCode);
	END $$
    
    CREATE FUNCTION getBiggestEvent(isOver BOOLEAN)
	RETURNS VARCHAR(255)
	BEGIN
		DECLARE eventTitle VARCHAR(255);
		DECLARE numberOfAccount INT;
        
		SELECT e.title, COUNT(*) AS nbrOccurences INTO eventTitle, numberOfAccount
		FROM AccountRegisterToEvent link
		JOIN Event e ON e.event_id = link.event
        WHERE
			isOver OR (NOT isOver AND e.date > CURRENT_DATE())
		GROUP BY e.title
		ORDER BY nbrOccurences DESC
		LIMIT 1;
        IF eventTitle IS NULL THEN
			RETURN "Nobody is link to an event :((";
		ELSE
			RETURN CONCAT("The biggest event is ", eventTitle, " with ", numberOfAccount, " accounts link.");
		END IF;
	END $$

DELIMITER ;
