# In this file you must implement your main query methods
# so they can be used by your database models to interact with your bot.

import os
import pymysql.cursors
from enum import Enum

# note that your remote host where your database is hosted
# must support user permissions to run stored triggers, procedures and functions.
db_host = os.environ["DB_HOST"]
db_username = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]

COLOR_GREEN = "\033[1;32;40m"
COLOR_WHITE = "\033[1;37;40m"


class Database:

  def connect(self):
    """
        This method creates a connection with your database
        IMPORTANT: all the environment variables must be set correctly
                   before attempting to run this method. Otherwise, it
                   will throw an error message stating that the attempt
                   to connect to your database failed.
        """
    try:
      conn = pymysql.connect(host=db_host,
                             port=3306,
                             user=db_username,
                             password=db_password,
                             db=db_name,
                             charset="utf8mb4",
                             cursorclass=pymysql.cursors.DictCursor)
      print("Bot connected to database {}".format(db_name))
      return conn
    except ConnectionError as err:
      print(f"An error has occurred: {err.args[1]}")
      print("\n")

  #TODO: needs to implement the internal logic of all the main query operations
  def get_response(self, query, values=None, fetch=False, many_entities=False):
    """
        query: the SQL query with wildcards (if applicable) to avoid injection attacks
        values: the values passed in the query
        fetch: If set to True, then the method fetches data from the database (i.e with SELECT)
        many_entities: If set to True, the method can insert multiple entities at a time.
        """
    connection = self.connect()
    # your code here
    response = None
    try:
      with connection.cursor() as cursor:
        if values:
          cursor.execute(query, values)
        else:
          cursor.execute(query)

        if fetch:
          if many_entities:
            response = cursor.fetchall()
          else:
            response = cursor.fetchone()
        else:
          connection.commit()
          response = "Query executed successfully."

        return response

    except pymysql.Error as e:
      print(f"Error executing query: {e}")
      return e

    finally:
      connection.close()

  @staticmethod
  def select(query, values=None, fetch=True, many_entities=False):
    database = Database()
    return database.get_response(query,
                                 values=values,
                                 fetch=fetch,
                                 many_entities=many_entities)

  @staticmethod
  def insert(query, values=None, many_entities=False):
    database = Database()
    return database.get_response(query,
                                 values=values,
                                 many_entities=many_entities)

  @staticmethod
  def update(query, values=None):
    database = Database()
    return database.get_response(query, values=values)

  @staticmethod
  def delete(query, values=None):
    database = Database()
    return database.get_response(query, values=values)

  @staticmethod
  def init_trigger():
    print(f"[{COLOR_GREEN}INIT TRIGGER{COLOR_WHITE}]: start")
    database = Database()
    database.delete(Queries.DROP_TRIGGER_INSERT_USER.value)
    database.delete(Queries.DROP_TRIGGER_DELETE_USER.value)
    database.insert(Queries.CREATE_TRIGGER_INSERT_USER.value)
    database.insert(Queries.CREATE_TRIGGER_DELETE_USER.value)
    print(f"[{COLOR_GREEN}INIT TRIGGER{COLOR_WHITE}]: end")

  @staticmethod
  def init_function():
    print(f"[{COLOR_GREEN}INIT FUNCTION{COLOR_WHITE}]: start\n")
    database = Database()
    database.delete(Queries.DROP_FUNCTION_GET_BIGGEST_EVENT.value)
    database.delete(Queries.DROP_FUNCTION_GET_OR_CREATE_LANGUAGE_ID.value)
    database.delete(Queries.DROP_FUNCTION_GET_OR_CREATE_OS_ID.value)
    database.delete(Queries.DROP_FUNCTION_GET_OR_CREATE_REGION_ID.value)
    database.insert(Queries.CREATE_FUNCTION_GET_BIGGEST_EVENT.value)
    print(f"[{COLOR_GREEN}INIT FUNCTION{COLOR_WHITE}]: end")
    database.insert(Queries.CREATE_FUNCTION_GET_OR_CREATE_LANGUAGE_ID.value)
    print(f"[{COLOR_GREEN}INIT PROCEDURE{COLOR_WHITE}]: start")
    database.insert(Queries.CREATE_FUNCTION_GET_OR_CREATE_OS_ID.value)
    database.insert(Queries.CREATE_FUNCTION_GET_OR_CREATE_REGION_ID.value)
    print(f"[{COLOR_GREEN}INIT PROCEDURE{COLOR_WHITE}]: end")

  @staticmethod
  def init_procedure():
    database = Database()
    database.delete(Queries.DROP_PROCEDURE_GET_EMAIL_REGION.value)
    database.insert(Queries.CREATE_PROCEDURE_GET_EMAIL_REGION.value)


class Queries(Enum):
  USER = """
          SELECT u.user_id, u.name, u.date_of_birth, a.account_id, region.name as \"Region\", os.name as \"OS\", l.name as \"Language\"
          FROM User u
          LEFT JOIN Account a ON a.user_id = u.user_id
          LEFT JOIN Region region ON region.region_id = a.region
          LEFT JOIN OS os ON os.os_id = a.os
          LEFT JOIN Language l ON l.language_id = a.language
          WHERE email = %s AND password = %s;
"""
  EVENTS = """
    SELECT * FROM Event WHERE date > DATE_SUB(CURDATE(), INTERVAL 7 DAY);
  """
  EVENTS_PASSED = "SELECT * FROM Event;"
  SOCIAL_SECURITY = """
    SELECT u.name as User, s.value as SocialSecurityNumber
    FROM User u
    JOIN SocialNumber s ON s.user = u.user_id
    WHERE email = %s AND password = %s;
    """
  CREATE_USER = """
    INSERT INTO User (name, email, password, date_of_birth) VALUES (%s, %s, %s, %s);
    """
  CREATE_ACCOUNT = """
    INSERT INTO Account (user_id, role, region, user_health_data, language, os)
    SELECT u.user_id, NULL, getOrCreateRegionId(%s, %s), NULL, getOrCreateLanguageId(%s, %s), getOrCreateOSId(%s, %s)
    FROM User u
    WHERE u.email = %s AND u.password = %s;
    """
  CREATE_SPORT_ACTIVITY = """
    INSERT INTO SportActivity (title, description, duration, user)
    SELECT %s, %s, %s, u.user_id
    FROM Account a
    JOIN User u ON u.user_id = a.user_id
    WHERE a.account_id = %s;
  """
  CREATE_MEAL = """
    INSERT INTO Meal (title, description, caloric_value, date, user)
    SELECT %s, %s, %s, %s, u.user_id
    FROM Account a
    JOIN User u ON u.user_id = a.user_id
    WHERE a.account_id = %s;
  """
  CREATE_EVENT = "INSERT INTO Event (title, description, date, place) VALUES (%s, %s, %s, %s);"
  LINK_ACCOUNT_TO_EVENT = "INSERT INTO AccountRegisterToEvent (account, event) VALUES (%s, %s);"
  UPDATE_USER = """
    UPDATE User
    JOIN SocialNumber s ON s.user = User.user_id
    SET User.name = %s, User.date_of_birth = %s, s.value = %s
    WHERE User.email = %s AND User.password = %s;
  """
  UPDATE_ACCOUNT = """
    UPDATE User
    JOIN Account a ON a.user_id = User.user_id
    SET a.region = getOrCreateRegionId(%s, %s), a.language = getOrCreateLanguageId(%s, %s), a.os = getOrCreateOSId(%s, %s)
    WHERE User.email = %s AND User.password = %s;
  """
  DELETE_USER = """
    DELETE u, s
    FROM SocialNumber s
    JOIN User u ON u.user_id = s.user
    WHERE s.value = %s;
  """
  DELETE_ACCOUNT = """
    DELETE a
    FROM Account a
    JOIN User u ON u.email = %s AND u.password = %s
    WHERE a.user_id = u.user_id;
  """
  BIGGEST_EVENT = "SELECT getBiggestEvent(%s);"
  REGION_USERS = "CALL GetUserEmailsByRegion(%s);"
  FIND_SUBSTRING_EVENT = "SELECT * FROM Event e WHERE e.title REGEXP TRIM(%s);"
  FIND_AVERAGE_AGE_ALL_EVENTS = """
    SELECT AVG(TIMESTAMPDIFF(YEAR, u.date_of_birth, CURDATE())) AS age
    FROM AccountRegisterToEvent link
    JOIN Account a ON a.account_id = link.account
    JOIN User u ON u.user_id = a.user_id;
  """
  FIND_AVERAGE_AGE = """
    SELECT AVG(TIMESTAMPDIFF(YEAR, u.date_of_birth, CURDATE())) AS age
    FROM AccountRegisterToEvent link
    JOIN Account a ON a.account_id = link.account
    JOIN User u ON u.user_id = a.user_id
    JOIN Event e ON e.event_id = link.event
    WHERE e.date > DATE_SUB(CURDATE(), INTERVAL 7 DAY);
  """
  GET_SPECIFIC_USER = """
    SELECT u.user_id, u.name, u.email, u.password, u.date_of_birth, u.health_metric_data_id, u.role_id, s.value as SocialNumber
    FROM User u
    JOIN SocialNumber s ON s.user = u.user_id
    WHERE email = %s AND password = %s;
  """
  GET_SPECIFIC_ACCOUNT = """
    SELECT a.account_id, a.user_id, a.role, a.user_health_data, region.name as \"Region\", os.name as \"OS\", l.name as \"Language\"
    FROM User u
    JOIN Account a ON a.user_id = u.user_id
    JOIN Region region ON region.region_id = a.region
    JOIN OS os ON os.os_id = a.os
    JOIN Language l ON l.language_id = a.language
    WHERE email = %s AND password = %s;
  """
  GET_SPECIFIC_LINK = """
    SELECT *
    FROM AccountRegisterToEvent
    WHERE account = %s AND event = %s
    ORDER BY user_register_to_event_id DESC
    LIMIT 1;
  """
  GET_SPECIFIC_SPORT_ACTIVITY = """
    SELECT *
    FROM SportActivity
    WHERE title = %s AND description = %s AND duration = %s AND user = %s
    ORDER BY sport_activity_id DESC
    LIMIT 1;
  """
  GET_SPECIFIC_MEAL = """
    SELECT *
    FROM Meal
    WHERE title = %s AND description = %s AND caloric_value = %s AND date = %s AND user = %s
    ORDER BY meal_id DESC
    LIMIT 1;
  """
  DROP_TRIGGER_INSERT_USER = "DROP TRIGGER IF EXISTS CREATE_SOCIAL_SECURITY_NUMBER;"
  DROP_TRIGGER_DELETE_USER = "DROP TRIGGER IF EXISTS DELETE_USER_ACCOUNT;"
  CREATE_TRIGGER_INSERT_USER = """
    CREATE TRIGGER CREATE_SOCIAL_SECURITY_NUMBER AFTER INSERT ON User
    FOR EACH ROW
    BEGIN
      INSERT INTO SocialNumber (value, user)
      VALUES (NEW.email, NEW.user_id);
    END
  """
  CREATE_TRIGGER_DELETE_USER = """
    CREATE TRIGGER DELETE_USER_ACCOUNT BEFORE DELETE ON User
    FOR EACH ROW
    BEGIN
      DELETE FROM Account WHERE user_id = OLD.user_id;
    END
  """
  DROP_FUNCTION_GET_BIGGEST_EVENT = "DROP FUNCTION IF EXISTS getBiggestEvent;"
  DROP_FUNCTION_GET_OR_CREATE_REGION_ID = "DROP FUNCTION IF EXISTS getOrCreateRegionId;"
  DROP_FUNCTION_GET_OR_CREATE_OS_ID = "DROP FUNCTION IF EXISTS getOrCreateOSId;"
  DROP_FUNCTION_GET_OR_CREATE_LANGUAGE_ID = "DROP FUNCTION IF EXISTS getOrCreateLanguageId;"
  CREATE_FUNCTION_GET_BIGGEST_EVENT = """
    CREATE FUNCTION getBiggestEvent(isOver BOOLEAN)
    RETURNS VARCHAR(255)
    BEGIN
      DECLARE eventTitle VARCHAR(255);
      DECLARE numberOfAccount INT;
      SELECT e.title, COUNT(*) AS nbrOccurences INTO eventTitle, numberOfAccount
      FROM AccountRegisterToEvent link
      JOIN Event e ON e.event_id = link.event
      WHERE isOver OR (NOT isOver AND e.date > CURRENT_DATE())
      GROUP BY e.title
      ORDER BY nbrOccurences DESC
      LIMIT 1;
      IF eventTitle IS NULL THEN
        RETURN \"Nobody is link to an event :((\";
      ELSE
        RETURN CONCAT(\"The biggest event is \", eventTitle, \" with \", numberOfAccount, \" accounts link.\");
      END IF;
    END
  """
  CREATE_FUNCTION_GET_OR_CREATE_REGION_ID = """
  CREATE FUNCTION getOrCreateRegionId(regionCode VARCHAR(45), regionName VARCHAR(255))
  RETURNS INT
  BEGIN
    DECLARE regionId INT;
    SELECT region_id INTO regionId FROM Region WHERE name = regionName;
    IF regionId IS NULL THEN
      SELECT region_id INTO regionId FROM Region WHERE code_area = regionCode;
        IF regionId IS NULL THEN
          INSERT INTO Region (code_area, name) VALUES (regionCode, regionName);
          SELECT LAST_INSERT_ID() INTO regionId;
        END IF;
      END IF;
      RETURN regionId;
    END
  """
  CREATE_FUNCTION_GET_OR_CREATE_OS_ID = """
    CREATE FUNCTION getOrCreateOSId(osCode VARCHAR(45), osName VARCHAR(255))
    RETURNS INT
    BEGIN
      DECLARE osId INT;
      SELECT os_id INTO osId FROM OS WHERE name = osName;
      IF osId IS NULL THEN
        SELECT os_id INTO osId FROM OS WHERE code = osCode;
        IF osId IS NULL THEN
          INSERT INTO OS (code, name) VALUES (osCode, osName);
          SELECT LAST_INSERT_ID() INTO osId;
        END IF;
      END IF;
      RETURN osId;
    END
  """
  CREATE_FUNCTION_GET_OR_CREATE_LANGUAGE_ID = """
    CREATE FUNCTION getOrCreateLanguageId(languageCode VARCHAR(45), languageName VARCHAR(255))
    RETURNS INT
    BEGIN
      DECLARE languageId INT;
      SELECT language_id INTO languageId FROM Language WHERE name = languageName;
      IF languageId IS NULL THEN
        SELECT language_id INTO languageId FROM Language WHERE code = languageCode;
        IF languageId IS NULL THEN
          INSERT INTO Language (code, name) VALUES (languageCode, languageName);
          SELECT LAST_INSERT_ID() INTO languageId;
        END IF;
      END IF;
      RETURN languageId;
    END
  """
  DROP_PROCEDURE_GET_EMAIL_REGION = "DROP PROCEDURE IF EXISTS GetUserEmailsByRegion;"
  CREATE_PROCEDURE_GET_EMAIL_REGION = """
    CREATE PROCEDURE GetUserEmailsByRegion(IN regionCode VARCHAR(45))
    BEGIN
      SELECT u.email
      FROM Account a
      JOIN User u ON u.user_id = a.user_id
      WHERE a.region = (SELECT region_id FROM Region r WHERE r.name = regionCode);
    END
  """
