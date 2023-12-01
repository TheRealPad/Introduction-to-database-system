"""
The code below is just representative of the implementation of a Bot. 
However, this code was not meant to be compiled as it. It is the responsability 
of all the students to modifify this code such that it can fit the 
requirements for this assignments.
"""

import os
import discord
from discord.ext import commands
from models import *
from database import Database, Queries

TOKEN = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.all()

database = Database()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')
  Database.connect(bot.user)


@bot.command(
    name="test",
    description="write your database business requirement for this command here"
)
async def _test(ctx, arg1):
  testModel = TestModel(ctx, arg1)
  response = testModel.response()
  await ctx.send(response)


# TODO: complete the following tasks:
#       (1) Replace the commands' names with your own commands
#       (2) Write the description of your business requirement in the description parameter
#       (3) Implement your commands' methods.


@bot.command(name="user",
             description="To get user and it account informations")
async def _command1(ctx, *args):
  if len(args) != 2:
    await ctx.send("Need 2 parameters: email, password")
    return
  data = Database.select(Queries.USER.value, [args[0], args[1]], True)
  if data == None:
    await ctx.send(
        "There is an error with your arguments, I can't find the user... Or maybe you don't have an account ?"
    )
  await ctx.send(
      f"- user_id: {data['user_id']}\n- name: {data['name']}\n- date of birth: {data['date_of_birth']}\n- account: {data['account_id']}\n- region: {data['Region']}\n- OS: {data['OS']}\n- language: {data['Language']}\n"
  )


@bot.command(
    name="events",
    description=
    "To get all events, if is-over is true, it will display any events, if not, ony the events who aren't over"
)
async def _command2(ctx, *args):
  if len(args) != 1:
    await ctx.send("Need 1 parameters: is_over")
    return
  if args[0] == "True":
    data = Database.select(Queries.EVENTS_PASSED.value, [], True, True)
  else:
    data = Database.select(Queries.EVENTS.value, [], True, True)
  if not len(data):
    await ctx.send("no data.")
  else:
    formatted_list = "\n".join([str(item) for item in data])
    await ctx.send(formatted_list)


@bot.command(name="social-security",
             description="Get the social security number link to a user")
async def _command5(ctx, *args):
  if len(args) != 2:
    await ctx.send("Need 2 parameters: email, password")
    return
  data = Database.select(Queries.SOCIAL_SECURITY.value, [args[0], args[1]],
                         True)
  if data == None:
    await ctx.send("Bad email/password or not social security number")
    return
  await ctx.send(data)


@bot.command(
    name="create-user",
    description=
    "Create a new User entry link to it social security number (create it too)"
)
async def _command7(ctx, *args):
  if len(args) != 4:
    await ctx.send("Need 4 parameters: name, email, password, date of birth")
    return
  data = Database.insert(Queries.CREATE_USER.value,
                         [args[0], args[1], args[2], args[3]])
  if data != "Query executed successfully.":
    await ctx.send(f"Error creation: {data}")
    return
  data = Database.select(Queries.GET_SPECIFIC_USER.value, [args[1], args[2]],
                         True)
  await ctx.send("id: " + str(data['user_id']))


@bot.command(
    name="create-account",
    description=
    "Create a new Account link to a user, if the region, language or os names doesn't exist, create it in the database"
)
async def _command8(ctx, *args):
  if len(args) != 5:
    await ctx.send(
        "Need 5 parameters: email, password, region name, language name, os name"
    )
    return
  data = Database.insert(
      Queries.CREATE_ACCOUNT.value,
      [args[2], args[2], args[3], args[3], args[4], args[4], args[0], args[1]])
  if data != "Query executed successfully.":
    await ctx.send(f"Error creation: {data}")
    return
  data = Database.select(Queries.GET_SPECIFIC_ACCOUNT.value,
                         [args[0], args[1]], True)
  await ctx.send("id: " + str(data['account_id']))


@bot.command(
    name="create-sport-activity",
    description="Create new sport activity link to user from it account")
async def _command18(ctx, *args):
  if len(args) != 4:
    await ctx.send(
        "Need 4 parameters: title, description, duration, account id")
    return
  data = Database.insert(Queries.CREATE_SPORT_ACTIVITY.value,
                         [args[0], args[1], args[2], args[3]], True)
  if data != "Query executed successfully.":
    await ctx.send(f"Error creation: {data}")
    return
  data = Database.select(Queries.GET_SPECIFIC_SPORT_ACTIVITY.value,
                         [args[0], args[1], args[2], args[3]], True)
  await ctx.send("id: " + str(data['sport_activity_id']))


@bot.command(name="create-meal",
             description="Create new meal link to user from it account")
async def _command19(ctx, *args):
  if len(args) != 5:
    await ctx.send(
        "Need 5 parameters: title, description, caloric value, date and account id"
    )
    return
  data = Database.insert(Queries.CREATE_MEAL.value,
                         [args[0], args[1], args[2], args[3], args[4]], True)
  if data != "Query executed successfully.":
    await ctx.send(f"Error creation: {data}")
    return
  data = Database.select(Queries.GET_SPECIFIC_MEAL.value,
                         [args[0], args[1], args[2], args[3], args[4]], True)
  await ctx.send("id: " + str(data['meal_id']))


@bot.command(
    name="create-event",
    description="Create a new event in the database, the place is just a string"
)
async def _command9(ctx, *args):
  if len(args) != 4:
    await ctx.send("Need 4 parameters: title, description, date, place")
    return
  data = Database.insert(Queries.CREATE_EVENT.value,
                         [args[0], args[1], args[2], args[3]], True)
  if data != "Query executed successfully.":
    await ctx.send(f"Error creation: {data}")
    return
  data = Database.select(Queries.FIND_SUBSTRING_EVENT.value, [args[0]], True,
                         True)
  print(data)
  await ctx.send("id: " + str(data[-1]['event_id']))


@bot.command(name="link-account-to-event",
             description="Link an Account to an event")
async def _command10(ctx, *args):
  if len(args) != 2:
    await ctx.send("Need 2 parameters: account_id, event_id")
    return
  data = Database.insert(Queries.LINK_ACCOUNT_TO_EVENT.value,
                         [args[0], args[1]], True)
  if data != "Query executed successfully.":
    await ctx.send(f"Error creation: {data}")
    return
  data = Database.select(Queries.GET_SPECIFIC_LINK.value, [args[0], args[1]],
                         True)
  await ctx.send("id: " + str(data['user_register_to_event_id']))


@bot.command(
    name="update-user",
    description="Update a User name, birth date and it social security number")
async def _command11(ctx, *args):
  if len(args) != 5:
    await ctx.send(
        "Need 5 parameters: name, email, password, date of birth (YEAR-MONTH-DAY), social security number"
    )
    return
  data = Database.update(Queries.UPDATE_USER.value,
                         [args[0], args[3], args[4], args[1], args[2]])
  if data != "Query executed successfully.":
    await ctx.send(f"Error creation: {data}")
    return
  data = Database.select(Queries.GET_SPECIFIC_USER.value, [args[1], args[2]],
                         True)
  await ctx.send(data)


@bot.command(
    name="update-account",
    description=
    "Update Account link to a user, if the region, language or os names doesn't exist, create it in the database"
)
async def _command12(ctx, *args):
  if len(args) != 5:
    await ctx.send(
        "Need 5 parameters: email, password, region name, language name, os name"
    )
    return
  data = Database.update(
      Queries.UPDATE_ACCOUNT.value,
      [args[2], args[2], args[3], args[3], args[4], args[4], args[0], args[1]])
  if data != "Query executed successfully.":
    await ctx.send(f"Error creation: {data}")
    return
  data = Database.select(Queries.GET_SPECIFIC_ACCOUNT.value,
                         [args[0], args[1]], True)
  print(data)
  await ctx.send(data)


@bot.command(name="delete-user",
             description="Delete the User link to this ssn and it Account link"
             )
async def _command13(ctx, *args):
  if len(args) != 1:
    await ctx.send("Need 1 parameter: social security number")
    return
  data = Database.delete(Queries.DELETE_USER.value, [args[0]])
  if data != "Query executed successfully.":
    await ctx.send(f"Error creation: {data}")
    return
  await ctx.send(data)


@bot.command(name="delete-account",
             description="Delete the Account link to the given User")
async def _command14(ctx, *args):
  if len(args) != 2:
    await ctx.send("Need 2 parameters: email, password")
    return
  data = Database.delete(Queries.DELETE_ACCOUNT.value, [args[0], args[1]])
  if data != "Query executed successfully.":
    await ctx.send(f"Error creation: {data}")
    return
  await ctx.send(data)


@bot.command(name="region-users",
             description="Get all users emails link to a region")
async def _command15(ctx, *args):
  if len(args) != 1:
    await ctx.send("Need 1 parameter: region")
    return
  data = Database.select(Queries.REGION_USERS.value, [args[0]], True, True)
  if data == ():
    await ctx.send("No data found")
  else:
    await ctx.send(data)


@bot.command(
    name="biggest-event",
    description=
    "Get the events with the most user register to it and get the number of people register.If is-over is true, check every events or it will check only the events who aren't finish."
)
async def _command6(ctx, *args):
  if len(args) != 1:
    await ctx.send("Need 1 parameters: is_over")
    return
  data = Database.select(Queries.BIGGEST_EVENT.value,
                         [1 if args[0] == "True" else 0], True, True)
  result = ""
  try:
    result = data[0]['getBiggestEvent(0)']
  except:
    result = data[0]['getBiggestEvent(1)']
  await ctx.send(result)


@bot.command(name="events-substring",
             description="Find all events with the given word in their title")
async def _command16(ctx, *args):
  if len(args) != 1:
    await ctx.send("Need 1 parameters: is_over")
    return
  data = Database.select(Queries.FIND_SUBSTRING_EVENT.value, [args[0]], True,
                         True)
  if data == ():
    await ctx.send("No data found")
  else:
    await ctx.send(data)


@bot.command(
    name="event-average-age",
    description=
    "Find the average age of the users in an event, if is over is passed, check the passed events too"
)
async def _command17(ctx, *args):
  if len(args) != 1:
    await ctx.send("Need 1 parameters: is_over")
    return
  if args[0] == "True":
    data = Database.select(Queries.FIND_AVERAGE_AGE_ALL_EVENTS.value, [], True)
  else:
    data = Database.select(Queries.FIND_AVERAGE_AGE.value, [], True)
  age = data['age']
  await ctx.send(f'average user age register to an event: {age}')


Database.init_trigger()
Database.init_procedure()
Database.init_function()
bot.run(TOKEN)
