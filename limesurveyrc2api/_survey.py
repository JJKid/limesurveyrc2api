from collections import OrderedDict
from limesurveyrc2api.exceptions import LimeSurveyError

class _Survey(object):

    def __init__(self, api):
        self.api = api    
        
    def get_group_properties(self, group_id, group_properties):
        """
        Get group properties of a group of a survey        

        Parameters:
        :param group_id: ID of the group to fetch properties for.
        :type group_id: Integer
        :param group_properties: List of group properties to be retrieved
        :type group_properties: Array
        """

        method = "get_group_properties"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iGroupID", group_id),
            ("aGroupSettings", group_properties)
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid group ID",
                "Error: No group found",
                "No permission",
                "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is dict
        
        print("Group properties", response)
        return response

    def get_question_properties(self, question_id, settings=None):
        """
        Get the properties of a specified question from LimeSurvey.
        
        Uses cache to avoid repeated requests for the same question.

        Parameters:
        :param question_id: ID of the question to fetch properties for.
        :type question_id: Integer
        :param settings: List of specific settings to retrieve, or "all" for all settings.
        :type settings: List of strings or "all"
        """

        method = "get_question_properties"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iQuestionID", question_id),
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid question ID",
                "Error: No question found",
                "No permission",
                "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is dict
        
        print("Question properties", response)
        return response

    def list_groups(self, sid):
        """
        Get survey properties of a survey        

        Parameters:
        :param sid: ID of the survey to fetch groups for.
        :type sid: Integer     
        """

        method = "list_groups"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", sid)
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "Error: No survey found",
                "No permission",
                "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        
        print(f"Listed groups for survey {sid}", response)
        return response

    def list_questions(self, survey_id,
                       group_id=None, language=None):
        """
        Return a list of questions from the specified survey.

        Parameters
        :param survey_id: ID of survey to list questions from.
        :type survey_id: Integer
        :param group_id: ID of the question group to filter on.
        :type group_id: Integer
        :param language: Language of survey to return for.
        :type language: String
        """
        method = "list_questions"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", survey_id),
            ("iGroupID", group_id),
            ("sLanguage", language)
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "Error: Invalid language",
                "Error: IMissmatch in surveyid and groupid",
                "No questions found",
                "No permission",
                "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response

    def list_surveys(self, username=None):
        """
        List surveys accessible to the specified username.

        Parameters
        :param username: LimeSurvey username to list accessible surveys for.
        :type username: String
        """
        method = "list_surveys"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Invalid user",
                "No surveys found",
                "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response