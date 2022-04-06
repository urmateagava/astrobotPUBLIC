import database
import botfile
import xmlfile


def sendhoro():
    counter = 0
    if counter <= len(database.malling_list()):
        for user in database.malling_list():
            sign = database.take_sign(user)
            botfile.bot.send_message(user, xmlfile.astro(sign[0], 'today'))
            counter += 1
