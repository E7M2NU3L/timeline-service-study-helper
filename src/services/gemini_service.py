from apptypes import timeline_types

class PromptGenerator:
    def __init__(self, prompt_data: timeline_types.PromptTypes):
        self.prompt_data = prompt_data

    def generate_prompt(self) -> str:
        prompt = f"""
        Generate a structured study plan for a student with the following details:
        
        ## Personalization:
        - **Time Limit:** {self.prompt_data.timelimit.value}
        - **Education Level:** {self.prompt_data.education.value}
        - **Age:** {self.prompt_data.age}
        - **Preferred Study Hours per Day:** {self.prompt_data.studyHours}
        - **Preferred Study Time:** {self.prompt_data.studytime.value}

        ## Study Goals & Subjects:
        - **Prior Knowledge Level:** {self.prompt_data.prior.value}
        - **Exam Name:** {self.prompt_data.exam}
        - **Exam Date:** {self.prompt_data.examdate}

        ## Study Preferences:
        - **Preferred Study Method:** {self.prompt_data.method.value}
        - **Revision Frequency:** {self.prompt_data.revision.value}
        - **Break Preference:** {self.prompt_data.breaks.value}

        ## External Constraints:
        - **Available Hours on Weekends:** {self.prompt_data.availablehoursinWeekend}

        ### Instructions:
        1. The plan should be **well-structured** and **realistic**.
        2. Adjust the difficulty and pacing based on prior knowledge.
        3. Include **study topics**, **practice sessions**, and **revision schedules**.
        4. Suggest **break times** and **effective study techniques**.
        5. Ensure **flexibility** to accommodate external constraints.

        Provide the study plan in a **detailed, structured format**.
        """
        return prompt.strip()