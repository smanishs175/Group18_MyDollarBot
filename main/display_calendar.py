"""

@author: Shruti
"""
import helper


def run(call, bot):
    name, action, year, month, day = call.data.split(helper.calendar_1_callback.sep)
    date = helper.calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
    if action == "DAY":
        helper.date_range.append(date)
        # bot.send_message(
        #     chat_id=call.from_user.id,
        #     text=f"You have chosen {date.strftime('%d.%m.%Y')}",
        #     reply_markup=ReplyKeyboardRemove(),
        # )
        print(f"{helper.calendar_1_callback}: Day: {helper.date_range}")

    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=ReplyKeyboardRemove(),
        )
        #print(f"{helper.calendar_1_callback}: Cancellation")
    #print(helper.date_range)
