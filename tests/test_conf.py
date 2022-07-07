from unittest import TestCase
from unittest.mock import call, mock_open, patch

from nak.config import Config
from nak.settings import LOG_COLOR


class TestConfig(TestCase):
    def setUp(self):
        self.config = Config()
        self.config.email = 'test@29next.com'
        self.config.password = 'password'
        self.config.client_id = '123456'

    ####
    # read_config
    ####
    @patch('builtins.open', mock_open(read_data='yaml data'))
    @patch("yaml.load", autospec=True)
    @patch("nak.config.env_config", autospec=True)
    @patch("os.path.exists", autospec=True)
    def test_read_config_should_read_config_from_file_and_return_config_correctly(
        self, mock_patch_exists, mock_env, mock_load_yaml
    ):
        mock_patch_exists.return_value = True
        mock_load_yaml.return_value = expected_config = {
            'client_id': 123456
        }
        mock_env.side_effect = ['test@29next.com', 'password']

        configs, env = self.config.read_config()
        expected_env = {
            'email': 'test@29next.com',
            'password': 'password'
        }
        assert configs == expected_config
        assert env == expected_env

    ####
    # validate_config
    ####
    def test_validate_config_should_raise_error_we_expect(self):
        with self.assertRaises(TypeError) as error:
            self.config.client_id = None
            self.config.email = 'test@test.com'
            self.config.password = 1234
            self.config.validate_config()
        assert str(error.exception) == LOG_COLOR.ERROR.format(message='argument client_id is required.')

        with self.assertRaises(TypeError) as error:
            self.config.client_id = 123456
            self.config.email = None
            self.config.password = 1234
            self.config.validate_config()
        assert str(error.exception) == LOG_COLOR.ERROR.format(message='argument email is required.')

        with self.assertRaises(TypeError) as error:
            self.config.client_id = 123456
            self.config.email = 'test@test.com'
            self.config.password = None
            self.config.validate_config()
        assert str(error.exception) == LOG_COLOR.ERROR.format(message='argument password is required.')

        with self.assertRaises(TypeError) as error:
            self.config.client_id = None
            self.config.email = None
            self.config.password = None
            self.config.validate_config()
        assert str(error.exception) == LOG_COLOR.ERROR.format(
            message='argument client_id, email, password are required.')

    def test_validate_with_config_not_none_should_not_raise_error(self):
        assert self.config.validate_config()

    # ####
    # # write_config
    # ####
    @patch("yaml.dump", autospec=True)
    @patch("nak.config.Config.read_config", autospec=True)
    @patch("os.path.exists", autospec=True)
    def test_write_config_with_new_config_should_call_update_file_config_correctly(
        self, mock_patch_exists, mock_read_config, mock_dump_yaml
    ):
        mock_patch_exists.return_value = True
        mock_dump_yaml.return_value = 'yaml data'
        mock_read_config.return_value = {
            'client_id': 123456,
        }, {
            'email': 'test@29next.com',
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
                    'client_id': 56789,
                }, f)

            with open('.env') as env:
                assert env.writelines.mock_calls == [call('email=test@29next.com\npassword=password2')]

    ####
    # save
    ####
    @patch("nak.config.Config.write_config", auto_space=True)
    def test_save_config_with_validate_true_true_should_call_write_config(self, mock_write_config):
        self.config.save()
        mock_write_config.assert_called_once_with()

    @patch("nak.config.Config.write_config", auto_space=True)
    def test_save_config_with_validate_false_false_should_call_write_config(self, mock_write_config):
        self.config.client_id = None

        with self.assertRaises(TypeError) as error:
            self.config.save()

        assert str(error.exception) == LOG_COLOR.ERROR.format(message='argument client_id is required.')
        mock_write_config.assert_not_called()
