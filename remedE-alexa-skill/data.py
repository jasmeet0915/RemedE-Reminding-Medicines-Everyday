from gettext import gettext as _

WELCOME_MESSAGE = _(
    "Welcome, you can say Hello or Help. Which would you like to try?")
HELLO_MSG = _("Hello Python World from Classes!")
HELP_MSG = _("You can say hello to me! How can I help?")
GOODBYE_MSG = _("Goodbye!")
REFLECTOR_MSG = _("You just triggered {}")
ERROR = _("Sorry, I had trouble doing what you asked. Please try again.")


launch_welcome_message = "Welcome to remedy helper! I am here to help you adhere better to your medicines and " \
                       "make you more self aware. You can start by telling me your name and asking me to login!"

login_welcome_message = "Welcome {}, good to have you on board!"

set_permissions_message = "You don't have Permissions set for reminders, Please provide reminder permissions to " \
                          "the skill using the alexa app"


def get_description_response(med_name, generic_name, description):
    return "The generic name of " + med_name + " is " + generic_name + ". A brief description " \
                                                                    "is as stated, " + description


def get_remaining_stock_intent_response(med_data):
    speech = "Here is the current status of your medicines: "
    reorder_meds = []
    for med in med_data:
        speech = speech + med['name'] + " will last for " + str(med['days_left']) + " days. "
        if med['days_left'] <= 3:
            reorder_meds.append(med['name'])

    if not reorder_meds:
        speech = speech + ". None of the medicines seem to be running out in the near future!"
    else:
        speech = speech + "You seem to be running out of "
        for m in reorder_meds:
            speech = speech + m

    return speech, reorder_meds
