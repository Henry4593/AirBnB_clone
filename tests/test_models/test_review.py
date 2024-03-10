#!/usr/bin/python3
"""Defines unittests for models/review.py.

Unittest classes:
    **TestReview_instantiation
    **TestReview_save
    **TestReview_to_dict
"""
import os
import models
import unittest
from time import sleep
from models.review import Review
from datetime import datetime


class TestReview_instantiation(unittest.TestCase):
    """Unittests for Review class instantiation."""

    def test_no_args_instantiates(self):
        """Tests if Review can be instantiated without arguments."""
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        """Tests if new instances are stored in the storage model."""
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        """Tests if the id attribute is a public string."""
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        """Tests if the created_at attribute is a public datetime."""
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        """Tests if the updated_at attribute is a public datetime."""
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        """Tests that place_id is a public class attribute, not an instance
        attribute.
        """
        rev = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(rev))
        self.assertNotIn("place_id", rev.__dict__)

    def test_user_id_is_public_class_attribute(self):

        rev = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(rev))
        self.assertNotIn("user_id", rev.__dict__)

    def test_text_is_public_class_attribute(self):
        """Tests that text is a public class attribute, not an instance
        attribute.
        """
        rev = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(rev))
        self.assertNotIn("text", rev.__dict__)

    def test_two_reviews_unique_ids(self):
        rev1 = Review()
        rev2 = Review()
        self.assertNotEqual(rev1.id, rev2.id)

    def test_two_reviews_different_created_at(self):
        rev1 = Review()
        sleep(0.05)
        rev2 = Review()
        self.assertLess(rev1.created_at, rev2.created_at)

    def test_two_reviews_different_updated_at(self):
        rev1 = Review()
        sleep(0.05)
        rev2 = Review()
        self.assertLess(rev1.updated_at, rev2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        rev = Review()
        rev.id = "123456"
        rev.created_at = rev.updated_at = dt
        rev_str = rev.__str__()
        self.assertIn("[Review] (123456)", rev_str)
        self.assertIn("'id': '123456'", rev_str)
        self.assertIn("'created_at': " + dt_repr, rev_str)
        self.assertIn("'updated_at': " + dt_repr, rev_str)

    def test_args_unused(self):
        rev = Review(None)
        self.assertNotIn(None, rev.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_isofmt = dt.isoformat()
        rev = Review(id="345", created_at=dt_isofmt, updated_at=dt_isofmt)
        self.assertEqual(rev.id, "345")
        self.assertEqual(rev.created_at, dt)
        self.assertEqual(rev.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests for the Review class's save method."""

    @classmethod
    def setUp(self):
        """Temporarily renames file.json to avoid conflicts."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        """Restores file.json after tests."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        """Tests if saving a Review updates its updated_at timestamp."""
        rev = Review()
        sleep(0.05)
        first_updated_at = rev.updated_at
        rev.save()
        self.assertLess(first_updated_at, rev.updated_at)

    def test_two_saves(self):
        """Tests if saving a Review several times updates updated_at
        repeatedly.
        """
        rev = Review()
        sleep(0.05)
        first_updated_at = rev.updated_at
        rev.save()
        second_updated_at = rev.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        rev.save()
        self.assertLess(second_updated_at, rev.updated_at)

    def test_save_with_arg(self):
        """Tests if calling save with an argument raises a TypeError."""
        rev = Review()
        with self.assertRaises(TypeError):
            rev.save(None)

    def test_save_updates_file(self):
        """Tests if saving a Review writes its information to file.json."""
        rev = Review()
        rev.save()
        rev_id = "Review." + rev.id
        with open("file.json", "r") as f:
            self.assertIn(rev_id, f.read())


class TestReview_to_dict(unittest.TestCase):
    """Unittests for the Review class's to_dict method."""
    def test_to_dict_type(self):
        """Tests if to_dict returns a dictionary."""
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Tests if to_dict includes expected keys."""
        rev = Review()
        self.assertIn("id", rev.to_dict())
        self.assertIn("created_at", rev.to_dict())
        self.assertIn("updated_at", rev.to_dict())
        self.assertIn("__class__", rev.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Tests if to_dict includes dynamically added attributes."""
        rev = Review()
        rev.middle_name = "Holberton"
        rev.my_number = 98
        self.assertEqual("Holberton", rev.middle_name)
        self.assertIn("my_number", rev.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Tests if to_dict converts datetime attributes to strings."""
        rev = Review()
        rev_dict = rev.to_dict()
        self.assertEqual(str, type(rev_dict["id"]))
        self.assertEqual(str, type(rev_dict["created_at"]))
        self.assertEqual(str, type(rev_dict["updated_at"]))

    def test_to_dict_output(self):
        """Tests the exact output format of to_dict."""
        dt = datetime.today()
        rev = Review()
        rev.id = "123456"
        rev.created_at = rev.updated_at = dt
        dt_dict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(rev.to_dict(), dt_dict)

    def test_contrast_to_dict_dunder_dict(self):
        """Tests if to_dict differs from the __dict__ attribute."""
        rev = Review()
        self.assertNotEqual(rev.to_dict(), rev.__dict__)

    def test_to_dict_with_arg(self):
        """Tests if calling to_dict with an argument raises a TypeError."""
        rev = Review()
        with self.assertRaises(TypeError):
            rev.to_dict(None)


if __name__ == "__main__":
    unittest.main()
