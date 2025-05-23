from radarpipeline import Feature, FeatureGroup
from datetime import datetime
class ParticipantQuestionnaireStreaks(FeatureGroup):
    def __init__(self):
        super().__init__()
        self.name = "ParticipantQuestionnaireStreaks"
        self.description = "Streaks of questionnaire completion"
        self.features = [NumberOfDaysInStudy, NumberOfDaysCompletedDailyQuestionnaire, LongestStreakOfAnsweringQuestionnaires]

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
        df_daily = data.get_variable_data(self.required_input_data)
        first_day = df_daily.groupby('key.userId')['value.time'].min().reset_index()
        first_day['num_days_in_study'] = first_day['date'].apply(lambda x: datetime.now().date() - x)
        return first_day


class NumberOfDaysCompletedDailyQuestionnaire(Feature):
    def __init__(self):
        super().__init__()
        self.name = "NumberOfDaysCompletedDailyQuestionnaire"
        self.description = "Number of days completed daily questionnaire"
        self.required_input_data = ["questionnaire_response/ADHDSymptomsDaily"]

    def preprocess(self, data):
        return data

    def compute(self, data):
        df_daily = data.get_variable_data(self.required_input_data)
        num_completed_ques = df_daily.groupby('key.userId')['value.time'].count()
        num_completed_ques = num_completed_ques.reset_index()
        num_completed_ques.columns = ['key.userId', 'num_completed_questionnaires']
        return num_completed_ques


class LongestStreakOfAnsweringQuestionnaires(Feature):
    def __init__(self):
        super().__init__()
        self.name = "LongestStreakOfAnsweringQuestionnaires"
        self.description = "Longest streak of answering questionnaires"
        self.required_input_data = ["questionnaire_response/ADHDSymptomsDaily"]

    def preprocess(self, data):
        return data

    def get_streaks(self, arr):
        longest_current_streak = 0
        current_streak = 0
        last_val = None
        for val in arr:
            if last_val is None:
                current_streak += 1
                last_val = val
            else:
                if val - last_val == 1:
                    current_streak += 1
                else:
                    current_streak = 1
                if longest_current_streak < current_streak:
                    longest_current_streak = current_streak
                last_val = val
        return longest_current_streak

    def compute(self, data):
        df_daily = data.get_variable_data(self.required_input_data)
        df_daily['date']  = df_daily['value.time'].dt.date
        df_daily= df_daily.sort_values(['key.userId', 'date']).reset_index(drop=True)
        first_day = df_daily.groupby('key.userId')['date'].min().reset_index()
        first_day.columns = ['key.userId', 'day_one']
        df_daily = df_daily.merge(first_day)
        df_daily['days_since_enrolement'] = df_daily['date'] - df_daily['day_one']
        df_daily['days_since_enrolement'] = df_daily['days_since_enrolement'].apply(
            lambda x: x.total_seconds()//(24*3600) + 1)
        df_daily['next_day'] = df_daily.groupby('key.userId')['days_since_enrolement'].shift(-1)
        df_daily['day_diff'] = df_daily['next_day'] - df_daily['days_since_enrolement']
        df_streaks = df_daily.groupby(
            'key.userId')['days_since_enrolement'].apply(
                lambda x: self._get_streaks(x.values)).reset_index()
        df_streaks.columns = ['key.userId', 'longest_streak']
        return df_streaks
