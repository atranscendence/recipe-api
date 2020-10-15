from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_read(self):
        """Test waiting_for_db  when db is already avalible
         to connect online ones"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            # wait_for_db or function to wait for connection
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # decoretor overites time sleep to return True for faster test
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting_for_db when db is not avalible"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
