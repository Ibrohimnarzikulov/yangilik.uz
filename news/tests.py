from django.test import TestCase

from news.models import Category


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create()


    def test_category_creation(self):
        self.assertEqual(self,Category.name,"Sport")
        self.assertEqual(self,Category.name,"Mahalliy")




class ArticleModelTest(TestCase):
    pass