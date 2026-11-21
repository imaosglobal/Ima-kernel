import unittest
from learning.github_achievement_growth import ACHIEVEMENTS,build_opportunity_queue,principles
class TestGithubAchievementGrowth(unittest.TestCase):
    def test_known_set(self):
        names={x.name for x in ACHIEVEMENTS}
        self.assertTrue({"Pull Shark","Galaxy Brain","Pair Extraordinaire","Starstruck","Quickdraw","YOLO","Public Sponsor"}<=names)
    def test_pull_shark_is_first_real_work_opportunity(self):
        q=build_opportunity_queue(repository_health={"qa":True,"deploy":True})
        self.assertEqual(q[0]["name"],"Pull Shark")
        self.assertEqual(q[0]["status"],"READY")
    def test_no_fake_engagement(self):
        self.assertIn("Never buy/trade stars or solicit fake engagement.",principles())
if __name__=="__main__": unittest.main()
