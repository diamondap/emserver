from django.test import TestCase
import em.tests as tests

class RouterTest(TestCase):

    fixtures = tests.DB_FIXTURES

    def test_index(self):
        from em.models import Router
        router = Router.objects.all()[0]
        self.assertIsNotNone(router)

    def test_detail(self):
        pass

    def test_create(self):
        pass

    def test_edit(self):
        pass

    def test_delete(self):
        pass
