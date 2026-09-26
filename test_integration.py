import unittest
from metabase_jev import classify_card

class MetabaseTest(unittest.TestCase):
    def test_saved_question_result(self):
        class Client:
            def decide(self, text):
                return {'route':'yes','probability':0.91,'state_sha256':'abc'}
        rows = list(classify_card('https://metabase.example', 7, 'review', 'Good?',
                    fetch=lambda url: [{'review':'great'}], client=Client()))
        self.assertEqual('yes', rows[0]['jev_route'])
