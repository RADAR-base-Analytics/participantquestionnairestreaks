from radarpipeline import Feature, FeatureGroup
imp
class ParticipantQuestionnaireStreaks(FeatureGroup):
    def __init__(self):
        super().__init__()
        name = "ParticipantQuestionnaireStreaks"
        description = "Streaks of questionnaire completion"
        features = [NumberOfDaysInStudy, NumberOfDaysCompletedDailyQuestionnaire, LongestStreakOfAnsweringQuestionnaires]

    def process(self, data):
        return data

class NumberOfDaysInStudy(Feature):
    def __init__(self):
        super().__init__()
        self.name = "NumberOfDaysInStudy"
        self.description = "Number of days in the study"
        self.required_input_data = ["questionnaire_response/ADHDSymptomsDaily"]

    def preprocess(self, data):
        return data

    def compute(self, data):
        df = data.get_variable_data(self.required_input_data)


class NumberOfDaysCompletedDailyQuestionnaire(Feature):
    def __init__(self):
        super().__init__()
        self.name = "NumberOfDaysCompletedDailyQuestionnaire"
        self.description = "Number of days completed daily questionnaire"
        self.required_input_data = ["questionnaire_response/ADHDSymptomsDaily"]

class LongestStreakOfAnsweringQuestionnaires(Feature):
    def __init__(self):
        super().__init__()
        self.name = "LongestStreakOfAnsweringQuestionnaires"
        self.description = "Longest streak of answering questionnaires"
        self.required_input_data = ["questionnaire_response/ADHDSymptomsDaily"]
