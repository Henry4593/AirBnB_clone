#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    **TestBaseModel_instantiation
    **TestBaseModel_save
    **TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        base_mdl1 = BaseModel()
        base_mdl2 = BaseModel()
        self.assertNotEqual(base_mdl1.id, base_mdl2.id)

    def test_two_models_different_created_at(self):
        base_mdl1 = BaseModel()
        sleep(0.05)
        base_mdl2 = BaseModel()
        self.assertLess(base_mdl1.created_at, base_mdl2.created_at)

    def test_two_models_different_updated_at(self):
        base_mdl1 = BaseModel()
        sleep(0.05)
        base_mdl2 = BaseModel()
        self.assertLess(base_mdl1.updated_at, base_mdl2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        base_mdl = BaseModel()
        base_mdl.id = "123456"
        base_mdl.created_at = base_mdl.updated_at = dt
        base_mdl_str = base_mdl.__str__()
        self.assertIn("[BaseModel] (123456)", base_mdl_str)
        self.assertIn("'id': '123456'", base_mdl_str)
        self.assertIn("'created_at': " + dt_repr, base_mdl_str)
        self.assertIn("'updated_at': " + dt_repr, base_mdl_str)

    def test_args_unused(self):
        base_mdl = BaseModel(None)
        self.assertNotIn(None, base_mdl.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_isofmt = dt.isoformat()
        base_mdl = BaseModel(id="345", created_at=dt_isofmt, updated_at=dt_isofmt)
        self.assertEqual(base_mdl.id, "345")
        self.assertEqual(base_mdl.created_at, dt)
        self.assertEqual(base_mdl.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_isofmt = dt.isoformat()
        base_mdl = BaseModel("12", id="345", created_at=dt_isofmt, updated_at=dt_isofmt)
        self.assertEqual(base_mdl.id, "345")
        self.assertEqual(base_mdl.created_at, dt)
        self.assertEqual(base_mdl.updated_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        base_mdl = BaseModel()
        sleep(0.05)
        first_updated_at = base_mdl.updated_at
        base_mdl.save()
        self.assertLess(first_updated_at, base_mdl.updated_at)

    def test_two_saves(self):
        base_mdl = BaseModel()
        sleep(0.05)
        first_updated_at = base_mdl.updated_at
        base_mdl.save()
        second_updated_at = base_mdl.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        base_mdl.save()
        self.assertLess(second_updated_at, base_mdl.updated_at)

    def test_save_with_arg(self):
        base_mdl = BaseModel()
        with self.assertRaises(TypeError):
            base_mdl.save(None)

    def test_save_updates_file(self):
        base_mdl = BaseModel()
        base_mdl.save()
        base_mdl.id = "BaseModel." + base_mdl.id
        with open("file.json", "r") as f:
            self.assertIn(base_mdl.id, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        base_mdl = BaseModel()
        self.assertTrue(dict, type(base_mdl.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        base_mdl = BaseModel()
        self.assertIn("id", base_mdl.to_dict())
        self.assertIn("created_at", base_mdl.to_dict())
        self.assertIn("updated_at", base_mdl.to_dict())
        self.assertIn("__class__", base_mdl.to_dict())

    def test_to_dict_contains_added_attributes(self):
        base_mdl = BaseModel()
        base_mdl.name = "Holberton"
        base_mdl.my_number = 98
        self.assertIn("name", base_mdl.to_dict())
        self.assertIn("my_number", base_mdl.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        base_mdl = BaseModel()
        bm_dict = base_mdl.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        base_mdl = BaseModel()
        base_mdl.id = "123456"
        base_mdl.created_at = base_mdl.updated_at = dt
        dt_dict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(base_mdl.to_dict(), dt_dict)

    def test_contrast_to_dict_dunder_dict(self):
        base_mdl = BaseModel()
        self.assertNotEqual(base_mdl.to_dict(), base_mdl.__dict__)

    def test_to_dict_with_arg(self):
        base_mdl = BaseModel()
        with self.assertRaises(TypeError):
            base_mdl.to_dict(None)


if __name__ == "__main__":
    unittest.main()
