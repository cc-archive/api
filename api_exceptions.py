class AnswerXmlException(Exception):
    def __init__(self, id, message):
        Exception.__init__(self, id, message)

        self.error_id = id
        self.error_msg = message
        
class InvalidClassException(AnswerXmlException):
    def __init__(self):
        AnswerXmlException.__init__(self, 'invalidclass',
                           'An unknown license class was specified.')

class InvalidFieldValue(AnswerXmlException):
    def __init__(self, field, answer):
        AnswerXmlException.__init__(self, 'invalidanswer',
                     'An invalid value (%s) was specified for the field %s.'
                      % (answer, field))
