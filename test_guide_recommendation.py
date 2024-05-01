import unittest
import pandas as pd
from guide_recommendation import recommend_guides


class TestRecommendGuides(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'Project Title': ['Machine learning in finance', 'AI in healthcare', 'Deep learning for computer vision'],
            'Guide': ['Dr. C', 'Dr. A', 'Dr. B', ]
        })

    def test_recommend_guides(self):
        project_title = 'AI for finance'
        expected_output = pd.DataFrame({
            'Guide': ['Dr. A', 'Dr. B', 'Dr. C'],
            'index': [1, 0, 2]
        })

        expected_output = expected_output.reset_index(drop=True)
        actual_output = recommend_guides(project_title, self.df)
        print(actual_output)
        pd.testing.assert_series_equal(actual_output['index'], expected_output['index'])


if __name__ == '__main__':
    unittest.main()
