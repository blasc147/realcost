from django.test import TestCase
from realcost.views import RealCostView

class ViewTestCase(TestCase):
    def test_payment(self):
        realcost_instance = RealCostView()
        self.assertEqual(round(realcost_instance.payment(23000, 0.059, 48),2), 539.10)

    #def test_approximate_apr(self):
    #    realcost_instance = RealCostView()
    #    self.assertEqual(round(realcost_instance.approximate_dealership_apr(25000, 0.059, 48, 585.98),2), 5.90)
