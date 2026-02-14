from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict
from limesurveyrc2api.exceptions import LimeSurveyError

class _Question(object):

    def __init__(self, api):
        self.api = api
        self.cache = {}  # Cache para almacenar las propiedades y las opciones de respuesta

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
        
        # Cache the properties
        print("Question properties", response)
        return response

    def get_question_answers(self, question_id, language="en"):
        """
        Get the answer options for a specified question from LimeSurvey.

        Parameters:
        :param question_id: ID of the question to fetch answer options for.
        :type question_id: Integer
        :param language: Language of the survey.
        :type language: String
        """
        cache_key = f"answers_{question_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Utilizamos get_question_properties para obtener todas las propiedades de la pregunta
        question_properties = self.get_question_properties(question_id)

        # Dependiendo del tipo de pregunta, las opciones de respuesta podrían estar en diferentes campos
        answer_options = question_properties.get('answers', None) or question_properties.get('subquestions', [])

        # Cache the answer options
        self.cache[cache_key] = answer_options
        return answer_options

    def get_questions_with_answers_parallel(self, question_ids, language="en"):
        """
        Get both the properties and answer options of questions in parallel for a list of question IDs.
        Uses ThreadPoolExecutor to fetch both properties and answer options simultaneously.

        Parameters:
        :param question_ids: List of question IDs to fetch properties and answer options for.
        :type question_ids: List of integers
        :param language: Language of the survey for the answer options.
        :type language: String
        """
        with ThreadPoolExecutor() as executor:
            # Obtener las propiedades de las preguntas en paralelo
            futures_properties = [executor.submit(self.get_question_properties, qid) for qid in question_ids]
            results_properties = [f.result() for f in futures_properties]

            # Obtener las opciones de respuesta en paralelo
            futures_answers = [executor.submit(self.get_question_answers, qid, language) for qid in question_ids]
            results_answers = [f.result() for f in futures_answers]

        # Fusionar las propiedades y las opciones de respuesta
        questions_with_answers = []
        for i, qid in enumerate(question_ids):
            question_data = results_properties[i].copy()  # Copia las propiedades
            question_data['answer_options'] = results_answers[i]  # Agrega las opciones de respuesta
            questions_with_answers.append(question_data)

        return questions_with_answers

    def list_questions(self, survey_id, group_id=None, language=None):
        """
        Return a list of questions from the specified survey.

        Parameters:
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
                "Error: Mismatch in survey ID and group ID",
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
