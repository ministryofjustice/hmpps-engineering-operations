import json
import os


class HelperUtils:

    @staticmethod
    def print_handler(methodName, messageType):
        """ This methods is a helper which prints error and the method name"""
        if messageType == 'success':
            return("Method {} completed successfully".format(methodName))
        elif messageType == 'failed':
            return "Method {} failed to run operation".format(methodName)
