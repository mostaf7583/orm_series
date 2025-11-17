from django.test import TestCase
from .models import Category, Product


class CategoryModelTest(TestCase):

    def setUp(self):
        self.parent_category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        self.child_category = Category.objects.create(
            name="Phones",
            slug="phones",
            parent=self.parent_category
        )

    def test_category_creation(self):
        self.assertEqual(self.parent_category.name, "Electronics")
        self.assertEqual(self.parent_category.slug, "electronics")
        self.assertIsNone(self.parent_category.parent)

    def test_category_str(self):
        self.assertEqual(str(self.parent_category), "Electronics")

    def test_category_children_relationship(self):
        # Parent should have 1 child
        self.assertEqual(self.parent_category.children.count(), 1)
        self.assertEqual(self.parent_category.children.first(), self.child_category)

    def test_unique_slug(self):
        with self.assertRaises(Exception):
            Category.objects.create(name="Duplicate", slug="electronics")


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Computers",
            slug="computers"
        )

        self.product = Product.objects.create(
            category=self.category,
            name="Laptop X1",
            slug="laptop-x1",
            description="Powerful laptop",
            price=1500.00,
            stock=10,
            is_active=True
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Laptop X1")
        self.assertEqual(self.product.slug, "laptop-x1")
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.price, 1500.00)
        self.assertEqual(self.product.stock, 10)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Laptop X1")

    def test_product_related_name(self):
        # Category.products should include created product
        self.assertEqual(self.category.products.count(), 1)
        self.assertEqual(self.category.products.first(), self.product)

    def test_unique_product_slug(self):
        # Slug must be unique
        with self.assertRaises(Exception):
            Product.objects.create(
                category=self.category,
                name="Laptop X2",
                slug="laptop-x1",  # duplicate slug
                price=1400.00,
                stock=5
            )
