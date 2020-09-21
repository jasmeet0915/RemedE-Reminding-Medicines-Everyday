import logging
import gettext
from flask import Flask
import Utils

from ask_sdk_core.skill_builder import SkillBuilder, CustomSkillBuilder
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractRequestInterceptor, AbstractExceptionHandler)
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.services.reminder_management import Trigger, TriggerType, AlertInfo, SpokenInfo, SpokenText, \
    PushNotification, PushNotificationStatus, ReminderRequest, Recurrence, recurrence_freq
from ask_sdk_model.services import ServiceException
from ask_sdk_model import Directive, Intent, Slot, SlotConfirmationStatus
from ask_sdk_model.dialog.confirm_intent_directive import ConfirmIntentDirective
from ask_sdk_model.intent_confirmation_status import IntentConfirmationStatus
from ask_sdk_model.dialog.delegate_directive import DelegateDirective


from ask_sdk_model import Response
import data
from flask_ask_sdk.skill_adapter import SkillAdapter
import json
import datetime
import pytz

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

user_slot = "userName"
medicine_slot = "medicine"
REQUIRED_PERMISSIONS = ["alexa::alerts:reminders:skill:readwrite"]
TIME_ZONE_ID = "Asia/Kolkata"

app = Flask(__name__)
sb = CustomSkillBuilder(api_client=DefaultApiClient())


class LaunchRequestHandler(AbstractRequestHandler):
    """Launch Request Handler"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = "Welcome to remedy helper! I am here to help you adhere better to your medicines and " \
                       "make you more self aware. You can start by telling me your name and asking me to login!"

        return (handler_input.response_builder
                .speak(speak_output)
                .response)


class LoginIntentHandler(AbstractRequestHandler):
    """Handler for Login Intent"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("LoginIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        rb = handler_input.response_builder

        if user_slot in slots:
            username = slots[user_slot].value
            Utils.get_user_key(username=username)
            med_data = Utils.get_user_medicine_data()

            if med_data is None:
                speech = "Welcome {}, good to have you on board!".format(username)
                return rb.speak(speech).response
            else:
                # make user medicine data available as session attributes to create alarms ReminderIntentHandler
                handler_input.attributes_manager.session_attributes['med_data'] = med_data
                speech = "Welcome {}, good to have you on board! " \
                         "I found some medicines in your record, would you like to set a " \
                         "reminder for them?".format(username)
                return rb.speak(speech).ask(speech).response

        else:
            speech = "I could not catch your name, try again please"
            return rb.speak(speech).response


class CreateMedicineReminderHandler(AbstractRequestHandler):
    """Handler for creating medicine reminders using AMAZON.YesIntent"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        permissions = handler_input.request_envelope.context.system.user.permissions
        reminder_service = handler_input.service_client_factory.get_reminder_management_service()
        med_data = handler_input.attributes_manager.session_attributes['med_data']

        if not (permissions and permissions.consent_token):
            return (handler_input.response_builder
                    .speak("You don't have Permissions set for reminders, "
                           "Please provide reminder permissions to the skill using the alexa app")
                    .response)
        else:
            for med in med_data:
                med_name = med_data[med]['name']
                med_times = med_data[med]['times']
                for time in med_times:
                    time_now = datetime.datetime.now(pytz.timezone(TIME_ZONE_ID))

                    # get reminder time hour, minute and create reminder_time datetime object
                    time = time.split(':')
                    hour = int(time[0])
                    minute = int(time[1])
                    reminder_time = datetime.datetime(year=time_now.year, month=time_now.month, day=time_now.day,
                                                      hour=hour, minute=minute, tzinfo=pytz.timezone(TIME_ZONE_ID))
                    time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S")
                    notification_time = reminder_time.strftime("%Y-%m-%dT%H:%M:%S")

                    recurrence = Recurrence(freq=recurrence_freq.RecurrenceFreq.DAILY)

                    trigger = Trigger(TriggerType.SCHEDULED_ABSOLUTE, scheduled_time=notification_time,
                                      time_zone_id=TIME_ZONE_ID, recurrence=recurrence)
                    text = SpokenText(locale='en-US', text='Time to take your medicine {}'.format(med_name))
                    alert_info = AlertInfo(SpokenInfo([text]))
                    push_notification = PushNotification(PushNotificationStatus.ENABLED)

                    # generate the reminder request object
                    reminder_request = ReminderRequest(request_time=time_now, trigger=trigger,
                                                       alert_info=alert_info, push_notification=push_notification)

                    print(reminder_request)
                    reminder_response = reminder_service.create_reminder(reminder_request, full_response=True)

        return (handler_input.response_builder
                .speak("Reminders have been successfully created for all your medicines!")
                .response)


class GetMedDataIntentHandler(AbstractRequestHandler):
    """Handler for GetMedDataIntent"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetMedDataIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots

        if medicine_slot in slots:
            med_name = slots[medicine_slot].value
            med_data = Utils.get_med_json_data(med_name)
            speech = "The generic name of " + med_name + " is " + med_data['generic_name'] + ". A brief description " \
                                                                                             "is as stated, " + \
                     med_data['description']
        else:
            speech = "I could not understand the name of the medicine, try again please"

        return (handler_input.response_builder
                .speak(speech)
                .response)


class GetSideEffectsIntentHandler(AbstractRequestHandler):
    """Handler for GetSideEffectsIntent"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetSideEffectsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots

        if medicine_slot in slots:
            med_name = slots[medicine_slot].value
            med_data = Utils.get_med_json_data(med_name)
            speech = "The side effects of " + med_name + " are " + med_data['side_effects']
        else:
            speech = "I could not understand the name of the medicine, try again please"

        return (handler_input.response_builder
                .speak(speech)
                .response)


class GetNextDoseIntentHandler(AbstractRequestHandler):
    """Handler for GetNextDoseIntent"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetNextDoseIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots

        if medicine_slot in slots:
            med_name = slots[medicine_slot].value
            next_dose_time = Utils.get_next_dose(med_name)
            speech = "Your upcoming dose for the medicine " + med_name + " is at " + str(next_dose_time)
        else:
            speech = "I was not able to find that medicine in your records please try again"

        return (handler_input.response_builder
                .speak(speech)
                .response)


class GetRemainingStockIntentHandler(AbstractRequestHandler):
    """Handler for GetRemainingStockIntent"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetRemainingStockIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        curr_req = handler_input.request_envelope.request
        reorder_intent = Intent(name="ReorderMedicinesIntent", slots={},
                                confirmation_status=IntentConfirmationStatus.NONE)
        reorder_intent_directive = DelegateDirective(reorder_intent)

        med_data = Utils.get_user_medicine_data('atrovent')
        current_intent = Intent(name=curr_req.intent.name, slots=curr_req.intent.slots,
                                confirmation_status=curr_req.intent.confirmation_status)
        confirm_intent_directive = DelegateDirective(current_intent)
        speech = "The remaining stock for your medicine " + med_data['name'] + " is " + str(med_data['remaining_stock'])
        print(curr_req.intent.confirmation_status)

        if curr_req.intent.confirmation_status == IntentConfirmationStatus.CONFIRMED:
            handler_input.request_envelope.request.dialog_state = 'COMPLETED'

        if handler_input.request_envelope.request.dialog_state != "COMPLETED":
            return (handler_input.response_builder
                    .add_directive(confirm_intent_directive)
                    .speak(speech)
                    .response)
        else:
            return (handler_input.response_builder
                    .speak(speech)
                    .add_directive(reorder_intent_directive)
                    .response)


class ReorderMedicinesIntentHandler(AbstractRequestHandler):
    """Handler for ReorderMedicinesIntent chained with GetRemainingStockIntent"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ReorderMedicinesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Union[None, Response]
        speech = "I am reordering medicines for you"
        return (handler_input.response_builder
                .speak(speech)
                .response)


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.HELP_MSG)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.GOODBYE_MSG)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = _(data.REFLECTOR_MSG).format(intent_name)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.ERROR)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data
    """

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        i18n = gettext.translation(
            'data', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes["_"] = i18n.gettext


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(LoginIntentHandler())
sb.add_request_handler(CreateMedicineReminderHandler())
sb.add_request_handler(GetMedDataIntentHandler())
sb.add_request_handler(GetSideEffectsIntentHandler())
sb.add_request_handler(GetNextDoseIntentHandler())
sb.add_request_handler(GetRemainingStockIntentHandler())
sb.add_request_handler(ReorderMedicinesIntentHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())

sb.add_exception_handler(CatchAllExceptionHandler())

skill_response = SkillAdapter(skill=sb.create(), skill_id="amzn1.ask.skill.cd33a56e-3c27-409e-aa97-8e24a2f0d8da",
                              app=app)
skill_response.register(app=app, route="/")

if __name__ == "__main__":
    app.run(debug=True)
