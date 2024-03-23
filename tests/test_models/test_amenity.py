#!/usr/bin/python3
"""Defines unittests for models/amenity.py."""
import os
import pep8
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.amenity import Amenity
from models.engine.db_storage import DBStorage


class TestAmenity(unittest.TestCase):
    """Unittests for testing the Amenity class."""

    @classmethod
    def setUpClass(cls):
        """Amenity testing setup."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        """Amenity testing teardown."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/amenity.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(Amenity.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        amenity = Amenity(name="The Andrew Lindburg treatment")
        self.assertEqual(str, type(amenity.id))
        self.assertEqual(datetime, type(amenity.created_at))
        self.assertEqual(datetime, type(amenity.updated_at))
        self.assertTrue(hasattr(amenity, "__tablename__"))
        self.assertTrue(hasattr(amenity, "name"))
        self.assertTrue(hasattr(amenity, "place_amenities"))

    def test_is_subclass(self):
        """Check that Amenity is a subclass of BaseModel."""
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_init(self):
        """Test initialization."""
        amenity = Amenity()
        self.assertIsInstance(amenity, Amenity)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.utcnow()
        amenity = Amenity("1", id="5", created_at=dt.isoformat())
        self.assertEqual(amenity.id, "5")
        self.assertEqual(amenity.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        amenity = Amenity(name="The Andrew Lindburg treatment")
        s = amenity.__str__()
        self.assertIn("[Amenity] ({})".format(amenity.id), s)
        self.assertIn("'id': '{}'".format(amenity.id), s)
        self.assertIn("'created_at': {}".format(repr(amenity.created_at)), s)
        self.assertIn("'updated_at': {}".format(repr(amenity.updated_at)), s)
        self.assertIn("'name': '{}'".format(amenity.name), s)

    def test_to_dict(self):
        """Test to_dict method."""
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertEqual(dict, type(amenity_dict))
        self.assertEqual(amenity.id, amenity_dict["id"])
        self.assertEqual("Amenity", amenity_dict["__class__"])
        self.assertEqual(amenity.created_at.isoformat(),
                         amenity_dict["created_at"])
        self.assertEqual(amenity.updated_at.isoformat(),
                         amenity_dict["updated_at"])
        self.assertEqual(amenity.name, amenity_dict["name"])


if __name__ == "__main__":
    unittest.main()

