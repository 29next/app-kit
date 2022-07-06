import unittest
from unittest.mock import MagicMock, call, mock_open, patch

from nak.command import Command


class TestCommand(unittest.TestCase):
    @patch("yaml.load", autospec=True)
    @patch('nak.command.Gateway', autospec=True)
    def setUp(self, mock_gateway, mock_load_yaml):
        mock_load_yaml.return_value = {}

        config = {
            'env': 'development',
            'user_email': 'test@29next.com',
            'password': 'password',
            'client_id': '123456',
        }
        with patch('builtins.open', mock_open(read_data='yaml data')):
            self.parser = MagicMock(**config)
            self.command = Command()

            self.mock_file = mock_open(read_data='test data')
            self.mock_gateway = mock_gateway

    #####
    # setup
    #####
    def test_setup_command_with_not_fill_any_parser_should_raise_error_with_argument_required(self):
        with self.assertRaises(TypeError) as error:
            self.parser.user_email = None
            self.parser.password = None
            self.parser.client_id = None
            self.command.setup(self.parser)

        assert str(error.exception) == (
            '[development] argument -u/--user_email, -p/--password, -c/--client_id are required.')

    @patch("nak.command.Config.write_config", autospec=True)
    def test_setup_with_parser_valid_should_call_create_config_and_env_file_correctly(self, mock_write_config):
        with self.assertLogs(level='INFO') as log:
            self.command.setup(self.parser)

        assert log.output == ['INFO:root:[development] App with client_id[123456] has been setup successfully.']

        # first call in parser_config at decorator
        # second call in command setup
        assert mock_write_config.call_count == 2

    #####
    # build
    #####
    @patch("os.path.exists", autospec=True)
    @patch("nak.command.zipfile", autospec=True)
    @patch("nak.command.get_all_file", autospec=True)
    @patch("nak.command.Config.write_config", autospec=True)
    def test_build_with_wrong_directory_should_raise_error_correctly(
        self, mock_write_config, mock_get_file, mock_zipfile, mock_path_exists
    ):
        mock_get_file.return_value = ["test1.file", "test2.file"]
        mock_path_exists.side_effect = [
            # check config at read_config
            False,
            # check envfile at read_config
            True,
            # check config dir at build command
            False,
            # check env file at build command
            False
        ]

        with self.assertRaises(TypeError) as error:
            self.command.build(self.parser)

        assert str(error.exception) == ('[development] Please check you is in correct directory.')
        assert mock_zipfile.mock_calls == []

    @patch("os.getcwd")
    @patch("os.path.exists")
    @patch("nak.conf.ZIP_DESTINATION")
    @patch("nak.command.zipfile", autospec=True)
    @patch("nak.command.get_all_file", autospec=True)
    @patch("nak.command.Config.write_config", autospec=True)
    def test_build_with_correct_directory_should_create_zip_file_correctly(
        self, mock_write_config, mock_get_file, mock_zipfile, mock_time, mock_path_exists, mock_current_path
    ):

        mock_get_file.return_value = ["test1.file", "test2.file"]
        mock_path_exists.side_effect = [
            # check config at read_config
            False,
            # check envfile at read_config
            False,
            # check config dir at build command
            True,
            # check env file at build command
            True
        ]

        mock_current_path.return_value = "/test-app"

        with self.assertLogs(level='INFO') as log:
            self.command.build(self.parser)

        assert mock_zipfile.ZipFile.return_value.mock_calls == [
            call.write('test1.file'),
            call.write('test2.file'),
            call.close(),
        ]
        assert log.output == ['INFO:root:[development] Build successfully.']

    #####
    # push
    #####
    @patch("os.path.exists", autospec=True)
    @patch("nak.command.get_all_file", autospec=True)
    @patch("nak.command.Config.write_config", autospec=True)
    def test_push_with_wrong_directory_should_raise_error_correctly(
        self, mock_write_config, mock_get_file, mock_path_exists
    ):
        mock_get_file.return_value = ["test1.file", "test2.file"]
        mock_path_exists.side_effect = [
            # check config at read_config
            False,
            # check envfile at read_config
            True,
            # check self dir at push command
            False
        ]

        with self.assertRaises(TypeError) as error:
            self.command.push(self.parser)

        assert str(error.exception) == ('[development] Please check you is in correct directory.')

    @patch("builtins.open", autospec=True)
    @patch("os.path.exists", autospec=True)
    @patch("nak.command.get_all_file", autospec=True)
    @patch("nak.command.Config.write_config", autospec=True)
    def test_push_with_correct_directory_should_call_gate_way_correctly(
        self, mock_write_config, mock_get_file, mock_path_exists, mock_open_file
    ):
        mock_get_file.return_value = ["test1-20200101010101.zip", "test2-20200101010102.zip"]
        mock_path_exists.side_effect = [
            # check config at read_config
            False,
            # check envfile at read_config
            True,
            # check self dir at push command
            True
        ]

        mock_open_file.return_value = file = MagicMock()

        with self.assertLogs(level='INFO') as log:
            self.command.push(self.parser)

        self.mock_gateway.return_value.update_app.assert_called_once_with(
            files={
                'file': ('test2-20200101010102.zip', file)
            }
        )
        assert log.output == [
            'INFO:root:[development] Pushing to app with client_id 123456',
            'INFO:root:[development] with filename test2-20200101010102.zip',
            'INFO:root:[development] by username test@29next.com',
            'INFO:root:[development] Push update file to app successfully.',
        ]
