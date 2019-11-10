# -*- coding: utf-8 -*-

import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Bienvenido al traductor a código morse, dime convierte seguido de lo que quieres que te convierta."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class ConvertToMorseIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ConvertToMorseIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        phrase = slots["phrase"]
        if phrase.value:
            morse_chars = Morse.convert(phrase.value)
            speak_output = \
                f"<speak>" \
                    f"<say-as interpret-as=\"characters\">" \
                        f"<prosody rate=\"slow\">" \
                            f"{morse_chars}" \
                        f"</prosody>" \
                    f"</say-as>" \
                f"</speak>"
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .set_should_end_session(True)
                    .response
            )
        else:
            return handler_input.response_builder.add_directive().response


class Morse:
    morse_map = {
        'A': [0, 1],
        'B': [1, 0, 0, 0],
        'C': [1, 0, 1, 0],
        'D': [1, 0, 0],
        'E': [0],
        'F': [0, 0, 1, 0],
        'G': [1, 1, 0],
        'H': [1, 1, 1, 1],
        'I': [0, 0],
        'J': [0, 1, 1, 1],
        'K': [1, 0, 1],
        'L': [0, 1, 0, 0],
        'M': [1, 1],
        'N': [1, 0],
        'O': [1, 1, 1],
        'P': [0, 1, 1, 0],
        'Q': [1, 1, 0, 1],
        'R': [0, 1, 0],
        'S': [0, 0, 0],
        'T': [1],
        'U': [0, 0, 1],
        'V': [0, 0, 0, 1],
        'W': [0, 1, 1],
        'X': [1, 0, 0, 1],
        'Y': [1, 0, 1, 1],
        'Z': [1, 0, 1, 1],
        '1': [0, 1, 1, 1, 1],
        '2': [0, 0, 1, 1, 1],
        '3': [0, 0, 0, 1, 1],
        '4': [0, 0, 0, 0, 1],
        '5': [0, 0, 0, 0, 0],
        '6': [1, 0, 0, 0, 0],
        '7': [1, 1, 0, 0, 0],
        '8': [1, 1, 1, 0, 0],
        '9': [1, 1, 1, 1, 0],
        '0': [1, 1, 1, 1, 1],
    }

    def convert(self_phrase):
        temp = ""
        self = self_phrase.upper()
        for i in self:
            if i == ' ':
                temp += ' '
            elif i in Morse.morse_map:
                temp += Morse.convert_letter(i)
            else:
                raise ValueError("El texto tiene un caracter no soportado.")
        return temp

    def convert_letter(letter):
        letter_value = Morse.morse_map.get(letter)
        morse_word = ""
        for i in letter_value:
            if i == 0:
                morse_word += '.'
            elif i == 1:
                morse_word += '-'
        return morse_word + ' '


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Para que te traduzca tu frase o palabra, necesito que digas, traduce y la frase."

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
        speak_output = "Adios!"

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
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

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

        speak_output = "Lo siento no he podido hacer lo que me has pedido, dimelo otra vez."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ConvertToMorseIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(
    IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
