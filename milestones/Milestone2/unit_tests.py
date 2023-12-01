# Discord API has a limited number of requests (bot requests) per day.
# If developers meet that quota, then Discord will put a temporal ban to your bot (24 hours)
# In order to avoid that, and only for testing, create unit test methods to test your functions
# without using the functionality provided by your bot. Once all your tests passed, then you can
# integrate these functions with your bot logic in main.py

import unittest
from database import Database, Queries
from datetime import date


class TestDatabaseConnectionMethods(unittest.TestCase):

  def test_user_1(self):
    data = Database.select(Queries.USER.value,
                           ["pdelgadoarevalo@sfsu.edu", "hehe"], True)
    self.assertTrue(data["user_id"] == 1)
    self.assertTrue(data["name"] == "Pierre-Alexandre")
    self.assertTrue(data["date_of_birth"] == date.fromisoformat('2002-02-14'))
    self.assertTrue(data["account_id"] == 1)
    self.assertTrue(data["Region"] == "California")
    self.assertTrue(data["OS"] == "linux")
    self.assertTrue(data["Language"] == "French")

  def test_user_2(self):
    data = Database.select(Queries.USER.value,
                           ["pdelgadoarevalo@sfsu.edu", "bad password"], True)
    self.assertTrue(data == None)

  def test_user_3(self):
    data = Database.select(Queries.USER.value, ["bad email", "hehe"], True)
    self.assertTrue(data == None)


class TestDatabaseEvents(unittest.TestCase):

  def test_events_1(self):
    data = Database.select(Queries.EVENTS.value, [], True)
    self.assertTrue(data == None)

  def test_events_2(self):
    data = Database.select(Queries.EVENTS_PASSED.value, [], True, True)
    self.assertTrue(len(data) >= 3)


class TestDatabaseSocialSecurityNumber(unittest.TestCase):

  def test_social_security_1(self):
    data = Database.select(Queries.SOCIAL_SECURITY.value,
                           ["pdelgadoarevalo@sfsu.edu", "hehe"], True)
    self.assertTrue(data["User"] == "Pierre-Alexandre")
    self.assertTrue(data["SocialSecurityNumber"] == "1")

  def test_social_security_2(self):
    data = Database.select(Queries.SOCIAL_SECURITY.value, ["bad", "data"],
                           True, True)
    self.assertTrue(data == ())


class TestDatabaseBiggestEvent(unittest.TestCase):

  def test_biggest_event_1(self):
    data = Database.select(Queries.BIGGEST_EVENT.value, [0], True)
    self.assertTrue(
        data['getBiggestEvent(0)'] == "Nobody is link to an event :((")

  def test_biggest_event_2(self):
    data = Database.select(Queries.BIGGEST_EVENT.value, [1], True)
    self.assertTrue(data['getBiggestEvent(1)'] ==
                    "The biggest event is Trail SF with 1 accounts link.")


class TestDatabaseRegionUser(unittest.TestCase):

  def test_region_user_1(self):
    data = Database.select(Queries.REGION_USERS.value, ["California"], True,
                           True)
    self.assertTrue(data == [{'email': 'pdelgadoarevalo@sfsu.edu'}])

  def test_region_user_2(self):
    data = Database.select(Queries.REGION_USERS.value, ["FAKE REGION"], True,
                           True)
    self.assertTrue(data == ())


class TestDatabaseFindSubstringEvent(unittest.TestCase):

  def test_find_substring_event_1(self):
    data = Database.select(Queries.FIND_SUBSTRING_EVENT.value, ["ai"], True,
                           True)
    self.assertTrue(data == [{
        'event_id': 1,
        'title': 'Trail SF',
        'description': 'Come run with me',
        'date': '2010-12-31 01:15:00',
        'place': 'San Francisco'
    }, {
        'event_id': 2,
        'title': 'Trail NY',
        'description': 'Come run with me',
        'date': '2010-12-31 01:15:00',
        'place': 'New York'
    }, {
        'event_id': 3,
        'title': 'Trail PA',
        'description': 'Come run with me',
        'date': '2010-12-31 01:15:00',
        'place': 'Paris'
    }])

  def test_find_substring_event_2(self):
    data = Database.select(Queries.FIND_SUBSTRING_EVENT.value, ["Trail SF"],
                           True, True)
    self.assertTrue(data == [{
        'event_id': 1,
        'title': 'Trail SF',
        'description': 'Come run with me',
        'date': '2010-12-31 01:15:00',
        'place': 'San Francisco'
    }])

  def test_find_substring_event_3(self):
    data = Database.select(Queries.FIND_SUBSTRING_EVENT.value,
                           ["    Trail SF    "], True, True)
    self.assertTrue(data == [{
        'event_id': 1,
        'title': 'Trail SF',
        'description': 'Come run with me',
        'date': '2010-12-31 01:15:00',
        'place': 'San Francisco'
    }])

  def test_find_substring_event_4(self):
    data = Database.select(Queries.FIND_SUBSTRING_EVENT.value, ["Bad title"],
                           True, True)
    self.assertTrue(data == ())


class TestDatabaseAverageAge(unittest.TestCase):

  def test_average_age_1(self):
    data = Database.select(Queries.FIND_AVERAGE_AGE.value, [], True)
    self.assertTrue(data['age'] == None)

  def test_average_age_2(self):
    data = Database.select(Queries.FIND_AVERAGE_AGE_ALL_EVENTS.value, [], True)
    self.assertTrue(data['age'] == 21.0000)


class TestDatabaseUserHandling(unittest.TestCase):

  def test_user_handling_1(self):
    data = Database.insert(
        Queries.CREATE_USER.value,
        ["pad", "delgadopierrealexandre@gmail.com", "123", "2002-02-14"], True)
    self.assertTrue(data == "Query executed successfully.")
    data = Database.insert(Queries.CREATE_ACCOUNT.value, [
        "CA", "CA", "French", "French", "Linux", "Linux",
        "delgadopierrealexandre@gmail.com", "123"
    ])
    self.assertTrue(data == "Query executed successfully.")
    data = Database.select(Queries.USER.value,
                           ["delgadopierrealexandre@gmail.com", "123"], True)
    self.assertTrue(data["name"] == "pad")
    self.assertTrue(data["Language"] == "French")
    data = Database.select(Queries.SOCIAL_SECURITY.value,
                           ["delgadopierrealexandre@gmail.com", "123"], True)
    self.assertTrue(data["User"] == "pad")
    self.assertTrue(
        data["SocialSecurityNumber"] == "delgadopierrealexandre@gmail.com")
    data = Database.update(Queries.UPDATE_USER.value, [
        "padou", "2002-02-14", "123", "delgadopierrealexandre@gmail.com", "123"
    ])
    self.assertTrue(data == "Query executed successfully.")
    data = Database.update(Queries.UPDATE_ACCOUNT.value, [
        "CA", "CA", "CI", "CI", "Linux", "Linux",
        "delgadopierrealexandre@gmail.com", "123"
    ])
    self.assertTrue(data == "Query executed successfully.")
    data = Database.select(Queries.SOCIAL_SECURITY.value,
                           ["delgadopierrealexandre@gmail.com", "123"], True)
    self.assertTrue(data["SocialSecurityNumber"] == "123")
    data = Database.select(Queries.USER.value,
                           ["delgadopierrealexandre@gmail.com", "123"], True)
    self.assertTrue(data["name"] == "padou")
    self.assertTrue(data["Language"] == "CI")

    data = Database.delete(Queries.DELETE_USER.value, ["123"])
    self.assertTrue(data == "Query executed successfully.")
    data = Database.select(Queries.USER.value,
                           ["delgadopierrealexandre@gmail.com", "123"], True)
    self.assertTrue(data == None)

  def test_user_handling_2(self):
    data = Database.insert(
        Queries.CREATE_USER.value,
        ["pad", "delgadopierrealexandre@gmail.com", "123", "2002-02-14"], True)
    self.assertTrue(data == "Query executed successfully.")
    data = Database.insert(Queries.CREATE_ACCOUNT.value, [
        "CA", "CA", "French", "French", "Linux", "Linux",
        "delgadopierrealexandre@gmail.com", "123"
    ])

    data = Database.delete(Queries.DELETE_ACCOUNT.value,
                           ["delgadopierrealexandre@gmail.com", "123"])
    self.assertTrue(data == "Query executed successfully.")
    data = Database.select(Queries.USER.value,
                           ["delgadopierrealexandre@gmail.com", "123"], True)
    self.assertTrue(data["account_id"] == None)
    data = Database.delete(Queries.DELETE_USER.value,
                           ["delgadopierrealexandre@gmail.com"])


class TestDatabaseSportActivityHandling(unittest.TestCase):

  def test_sport_activity_1(self):
    data = Database.insert(Queries.CREATE_SPORT_ACTIVITY.value,
                           ["Unit test", "Unit test", 10, 1], True)
    self.assertTrue(data == "Query executed successfully.")
    data = Database.select(Queries.GET_SPECIFIC_SPORT_ACTIVITY.value,
                           ["Unit test", "Unit test", 10, 1], True)
    self.assertTrue(
        data == {
            'sport_activity_id': 4,
            'title': 'Unit test',
            'description': 'Unit test',
            'duration': 10,
            'user': 1
        })


class TestDatabaseMealHandling(unittest.TestCase):

  def test_meal_1(self):
    data = Database.insert(Queries.CREATE_MEAL.value,
                           ["Unit test", "Unit test", 10, "1970/01/01", 1],
                           True)
    self.assertTrue(data == "Query executed successfully.")
    data = Database.select(Queries.GET_SPECIFIC_MEAL.value,
                           ["Unit test", "Unit test", 10, "1970/01/01", 1],
                           True)
    self.assertTrue(
        data == {
            'meal_id': 4,
            'title': 'Unit test',
            'description': 'Unit test',
            'caloric_value': 10,
            'date': '1970/01/01',
            'user': 1
        })


class TestDatabaseEventHandling(unittest.TestCase):

  def test_event_1(self):
    data = Database.insert(
        Queries.CREATE_EVENT.value,
        ["Unit test", "Unit test", "1970/01/01", "Unit test"], True)
    self.assertTrue(data == "Query executed successfully.")
    data = Database.select(Queries.FIND_SUBSTRING_EVENT.value, ["Unit test"],
                           True, True)
    self.assertTrue(len(data))


class TestDatabaseTrigger(unittest.TestCase):

  def test_trigger_1(self):
    Database.init_trigger()


if __name__ == '__main__':
  Database.init_trigger()
  Database.init_procedure()
  Database.init_function()
  unittest.main()
