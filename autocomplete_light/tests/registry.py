import unittest

from django.db import models

import autocomplete_light


class Foo(models.Model):
    pass


class Bar(autocomplete_light.AutocompleteModelBase):
    pass


class RegistryTestCase(unittest.TestCase):
    def setUp(self):
        self.registry = autocomplete_light.AutocompleteRegistry()

    def test_register_model(self):
        self.registry.register(Foo)
        self.assertIn('FooAutocomplete', self.registry.keys())

    def test_register_model_and_autocomplete(self):
        self.registry.register(Foo, Bar)
        self.assertIn('FooBar', self.registry.keys())

    def test_register_autocomplete(self):
        self.registry.register(Bar)
        self.assertIn('Bar', self.registry.keys())

    def test_unregister(self):
        self.registry.register(Bar)
        self.registry.unregister('Bar')
        self.assertEqual(self.registry.keys(), [])

    def test_register_with_kwargs(self):
        self.registry.register(Foo, search_name='search_name')
        self.assertEqual(self.registry['FooAutocomplete'].search_name,
            'search_name')

    def test_register_with_autocomplete_and_kwargs(self):
        self.registry.register(Foo, Bar, search_name='search_name')
        self.assertEqual(self.registry['FooBar'].search_name,
            'search_name')

    def test_register_with_custom_name(self):
        self.registry.register(Foo, Bar, name='BarFoo')
        self.assertIn('BarFoo', self.registry.keys())
        self.assertEqual(self.registry['BarFoo'].__name__, 'BarFoo')