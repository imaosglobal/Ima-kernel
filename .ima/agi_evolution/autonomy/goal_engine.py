class GoalEngine:

    def create_goal(self,name):
        return {
            "goal":name,
            "status":"created",
            "feedback":True
        }
