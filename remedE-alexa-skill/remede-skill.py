import logging
import gettext
from flask import Flask
import Utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractRequestInterceptor, AbstractExceptionHandler)
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
import data
from flask_ask_sdk.skill_adapter import SkillAdapter
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

user_slot = "userName"
medicine_slot = "medicine"

app = Flask(__name__)


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

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class LoginIntentHandler(AbstractRequestHandler):
    """Handler for Login Intent"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("LoginIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Union[None, Response]

        slots = handler_input.request_envelope.request.intent.slots

        if user_slot in slots:
            username = slots[user_slot].value
            Utils.get_user_key(username=username)
            speech = "Welcome {}, good to have you on board! " \
                     "I found some medicines in your record, would you like to set a " \
                     "reminder for them?".format(username)

        else:
            speech = "I could not catch your name, try again please"

        return (handler_input.response_builder
                .speak(speech)
                .ask(speech)
                .response)


class GetMedDataIntentHandler(AbstractRequestHandler):
    """Handler for GetMedDataIntent"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetMedDataIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Union[None, Response]

        slots = handler_input.request_envelope.request.intent.slots

        if medicine_slot in slots:
            med_name = slots[medicine_slot].value
            med_data = Utils.get_med_json_data(med_name)
            speech = "The generic name of " + med_name + " is " + med_data['generic_name'] + ". A brief description " \
                     "is as stated, " + med_data['description']
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
        # type: (HandlerInput) -> Union[None, Response]

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
        # type: (HandlerInput) -> Union[None, Response]

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
        # type: (HandlerInput) -> Union[None, Response]

        slots = handler_input.request_envelope.request.intent.slots

        if medicine_slot in slots:
            med_name = slots[medicine_slot].value
            remaining_stock = Utils.get_remaining_stock(med_name)
            speech = "The remaining stock for your medicine "+med_name+" is "+str(remaining_stock)
        else:
            speech = "I could not find that medicine in your records, please try again"

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


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(LoginIntentHandler())
sb.add_request_handler(GetMedDataIntentHandler())
sb.add_request_handler(GetSideEffectsIntentHandler())
sb.add_request_handler(GetNextDoseIntentHandler())
sb.add_request_handler(GetRemainingStockIntentHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())

sb.add_exception_handler(CatchAllExceptionHandler())

skill_response = SkillAdapter(skill=sb.create(), skill_id="amzn1.ask.skill.cd33a56e-3c27-409e-aa97-8e24a2f0d8da", app=app)
skill_response.register(app=app, route="/")


if __name__ == "__main__":
    app.run(debug=True)




