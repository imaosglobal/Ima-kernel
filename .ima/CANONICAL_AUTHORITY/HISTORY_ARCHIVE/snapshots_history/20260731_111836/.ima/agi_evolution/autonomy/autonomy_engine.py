class AutonomyEngine:

    def create_goal(self, objective):
        return {
            "goal": objective,
            "status":"created"
        }

    def evaluate(self,result):
        return {
            "feedback":result
        }
