#!/usr/bin/python3
"""Defines unittests for models/state.py.

Unittest classes:
    **TestState_instantiation
    **TestState_save
    **TestState_to_dict
"""
import os
import models
import unittest
from time import sleep
from models.state import State
from datetime import datetime


class TestState_instantiation(unittest.TestCase):
    """Unittests for State class instantiation."""

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        state_ = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(state_))
        self.assertNotIn("name", state_.__dict__)

    def test_two_states_unique_ids(self):
        state_1 = State()
        state_2 = State()
        self.assertNotEqual(state_1.id, state_2.id)

    def test_two_states_different_created_at(self):
        state_1 = State()
        sleep(0.05)
        state_2 = State()
        self.assertLess(state_1.created_at, state_2.created_at)

    def test_two_states_different_updated_at(self):
        state_1 = State()
        sleep(0.05)
        state_2 = State()
        self.assertLess(state_1.updated_at, state_2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        state_ = State()
        state_.id = "123456"
        state_.created_at = state_.updated_at = dt
        state_str = state_.__str__()
        self.assertIn("[State] (123456)", state_str)
        self.assertIn("'id': '123456'", state_str)
        self.assertIn("'created_at': " + dt_repr, state_str)
        self.assertIn("'updated_at': " + dt_repr, state_str)

    def test_args_unused(self):
        state_ = State(None)
        self.assertNotIn(None, state_.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_isofmt = dt.isoformat()
        state_ = State(id="345", created_at=dt_isofmt, updated_at=dt_isofmt)
        self.assertEqual(state_.id, "345")
        self.assertEqual(state_.created_at, dt)
        self.assertEqual(state_.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Unittests for the State class's save method."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

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
        """Tests if saving a State updates its updated_at timestamp."""
        state_ = State()
        sleep(0.05)
        first_updated_at = state_.updated_at
        state_.save()
        self.assertLess(first_updated_at, state_.updated_at)

    def test_two_saves(self):
        """Tests if saving a State twice updates updated_at multiple times."""
        state_ = State()
        sleep(0.05)
        first_updated_at = state_.updated_at
        state_.save()
        second_updated_at = state_.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        state_.save()
        self.assertLess(second_updated_at, state_.updated_at)

    def test_save_with_arg(self):
        """Tests if calling save with an argument raises a TypeError."""
        state_ = State()
        with self.assertRaises(TypeError):
            state_.save(None)

    def test_save_updates_file(self):
        """Tests if saving a State writes its information to file.json."""
        state_ = State()
        state_.save()
        state_id = "State." + state_.id
        with open("file.json", "r") as f:
            self.assertIn(state_id, f.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests for the State class's to_dict method."""

    def test_to_dict_type(self):
        """Tests if to_dict returns a dictionary."""
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Tests if to_dict includes expected keys."""
        state_ = State()
        self.assertIn("id", state_.to_dict())
        self.assertIn("created_at", state_.to_dict())
        self.assertIn("updated_at", state_.to_dict())
        self.assertIn("__class__", state_.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Tests if to_dict includes dynamically added attributes."""
        state_ = State()
        state_.middle_name = "Holberton"
        state_.my_number = 98
        self.assertEqual("Holberton", state_.middle_name)
        self.assertIn("my_number", state_.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Tests if to_dict converts datetime attributes to strings."""
        state_ = State()
        state_dict = state_.to_dict()
        self.assertEqual(str, type(state_dict["id"]))
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_to_dict_output(self):
        """Tests the exact output format of to_dict."""
        dt = datetime.today()
        state_ = State()
        state_.id = "123456"
        state_.created_at = state_.updated_at = dt
        dt_dict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(state_.to_dict(), dt_dict)

    def test_contrast_to_dict_dunder_dict(self):
        """Tests if to_dict differs from the __dict__ attribute."""
        state_ = State()
        self.assertNotEqual(state_.to_dict(), state_.__dict__)

    def test_to_dict_with_arg(self):
        """Tests if calling to_dict with an argument raises a TypeError."""
        state_ = State()
        with self.assertRaises(TypeError):
            state_.to_dict(None)


if __name__ == "__main__":
    unittest.main()
