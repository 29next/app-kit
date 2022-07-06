from unittest import TestCase
from unittest.mock import MagicMock, call, mock_open, patch

from nak.conf import Config


class TestConfig(TestCase):
    def setUp(self):
        config = {
            'env': 'development',
            'user_email': 'test@29next.com',
            'password': 'password',
            'client_id': '123456',
        }
        self.config = Config(**config)

    ####
    # parser_config
    ####
    def test_parser_config_should_set_config_config_correctly(self):
        new_config = {
            'env': 'development',
            'user_email': 'test2@29next.com',
            'password': 'password2',
            'client_id': '2223332',
        }
        parser = MagicMock(**new_config)

        with patch("nak.conf.Config.write_config") as mock_write_config:
            self.config.parser_config(parser=parser)

        self.assertEqual(self.config.user_email, new_config['user_email'])
        self.assertEqual(self.config.password, new_config['password'])
        self.assertEqual(self.config.client_id, new_config['client_id'])
        mock_write_config.assert_not_called()

        with patch("nak.conf.Config.write_config") as mock_write_config:
            self.config.parser_config(parser=parser, write_file=True)

        self.assertEqual(self.config.user_email, new_config['user_email'])
        self.assertEqual(self.config.password, new_config['password'])
        self.assertEqual(self.config.client_id, new_config['client_id'])
        mock_write_config.assert_called_once()

    ####
    # read_config
    ####
    @patch('builtins.open', mock_open(read_data='yaml data'))
    @patch("yaml.load", autospec=True)
    @patch("nak.conf.env_config", autospec=True)
    @patch("os.path.exists", autospec=True)
    def test_read_config_should_read_config_from_file_and_return_config_correctly(
        self, mock_patch_exists, mock_env, mock_load_yaml
    ):
        mock_patch_exists.return_value = True
        mock_load_yaml.return_value = expected_config = {
            "development": {
                'client_id': 123456
            }
        }
        mock_env.side_effect = ['test@29next.com', 'password']

        configs, env = self.config.read_config()
        expected_env = {
            'user_email': 'test@29next.com',
            'password': 'password'
        }
        assert configs == expected_config
        assert env == expected_env

    ####
    # validate_config
    ####
    def test_validate_config_should_raise_error_we_expect(self):
        self.config.client_id_required = self.config.user_email_required = self.config.password_required = True

        with self.assertRaises(TypeError) as error:
            self.config.client_id = None
            self.config.user_email = 'test@test.com'
            self.config.password = 1234
            self.config.validate_config()
        self.assertEqual(str(error.exception), '[development] argument -c/--client_id is required.')

        with self.assertRaises(TypeError) as error:
            self.config.client_id = 123456
            self.config.user_email = None
            self.config.password = 1234
            self.config.validate_config()
        self.assertEqual(str(error.exception), '[development] argument -u/--user_email is required.')

        with self.assertRaises(TypeError) as error:
            self.config.client_id = 123456
            self.config.user_email = 'test@test.com'
            self.config.password = None
            self.config.validate_config()
        self.assertEqual(str(error.exception), '[development] argument -p/--password is required.')

        with self.assertRaises(TypeError) as error:
            self.config.client_id = None
            self.config.user_email = None
            self.config.password = None
            self.config.validate_config()
        self.assertEqual(
            str(error.exception),
            '[development] argument -u/--user_email, -p/--password, -c/--client_id are required.')

    def test_validate_with_not_required_parser_config_should_not_raise_error(self):
        assert self.config.validate_config()

    ####
    # write_config
    ####
    @patch("yaml.dump", autospec=True)
    @patch("nak.conf.Config.read_config", autospec=True)
    @patch("os.path.exists", autospec=True)
    def test_write_config_with_new_config_should_call_update_file_config_correctly(
        self, mock_patch_exists, mock_read_config, mock_dump_yaml
    ):
        mock_patch_exists.return_value = True
        mock_dump_yaml.return_value = 'yaml data'
        mock_read_config.return_value = {
            'development': {
                'client_id': 123456,
            }
        }, {
            'user_email': 'test@29next.com',
            'password': 'password',
        }

        # new config
        self.config.client_id = 56789
        self.config.user_name = 'test2@test.com'
        self.config.password = "password2"

        # self.config.write_config()
        with patch('builtins.open', mock_open()):
            with open('config.yml') as f:
                self.config.write_config()
                mock_dump_yaml.assert_called_once_with({
                    'development': {'client_id': 56789},
                }, f)

            with open('.env') as env:
                assert env.writelines.mock_calls == [call('user_email=test@29next.com\npassword=password2')]

    ####
    # save
    ####
    @patch("nak.conf.Config.write_config", auto_space=True)
    def test_save_config_with_write_file_true_should_call_write_config(self, mock_write_config):
        self.config.save(write_file=True)
        mock_write_config.assert_called_once_with()

    @patch("nak.conf.Config.write_config", auto_space=True)
    def test_save_config_with_write_file_false_should_call_write_config(self, mock_write_config):
        self.config.save(write_file=False)
        mock_write_config.assert_not_called()
