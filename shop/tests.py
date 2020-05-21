from django.test import TestCase
from django.urls import reverse
from .models import Product, Category
# Create your tests here.


class HomepageTests(TestCase):
    def setUp(self):
        url = reverse('shop:product_list')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'shop/product/list.html')

    def test_contains_correct_html(self):
        self.assertContains(self.response, 'Categories')

    def test_does_not_contain(self):
        self.assertNotContains(self.response, 'I should not be here')


class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test', slug='test')

    def test_str(self):
        self.assertEqual(self.category.__str__(), self.category.name)

    def test_absolute_url(self):
        expected_url = reverse('shop:product_list_by_category', args=[self.category.slug])
        self.assertEqual(self.category.get_absolute_url(), expected_url)


class ModelTest(TestCase):
    def setUp(self):
        cate = Category.objects.create(name='test', slug='test')
        self.product = Product.objects.create(
            name='test',
            slug='test',
            category=cate,
            description='test product',
            price=500
        )

    def test_str(self):
        self.assertEqual(self.product.__str__(), self.product.name)

    def test_absolute_url(self):
        expected_url = reverse('shop:product_detail', args=[self.product.id, self.product.slug])
        self.assertEqual(self.product.get_absolute_url(), expected_url)












