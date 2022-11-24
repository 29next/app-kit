import unittest
from unittest.mock import MagicMock, call, mock_open, patch

from nak.command import Command
from nak.settings import LOG_COLOR


class TestCommand(unittest.TestCase):
    @patch("yaml.load", autospec=True)
    @patch('nak.command.Gateway', autospec=True)
    def setUp(self, mock_gateway, mock_load_yaml):
        mock_load_yaml.return_value = {}

        with patch('builtins.open', mock_open(read_data='yaml data')):
            self.command = Command()

            self.mock_file = mock_open(read_data='test data')
            self.mock_gateway = mock_gateway

    #####
    # setup
    #####
    @patch('builtins.input', autospec=True)
    def test_setup_command_with_not_fill_any_input_should_raise_error_with_argument_required(self, mock_input):
        mock_input.side_effect = [None, None, None]

        with self.assertRaises(TypeError) as error:
            self.command.setup()

        assert str(error.exception) == LOG_COLOR.ERROR.format(
            message='argument client_id, email, password are required.')

    @patch("nak.command.Config.write_config", autospec=True)
    @patch('builtins.input', autospec=True)
    def test_setup_command_with_not_fill_any_input_but_already_have_config_should_not_raise(
        self, mock_input, mock_write_config
    ):
        mock_input.side_effect = [None, None, None]
        self.command.config.client_id = '123456'
        self.command.config.email = 'test@29next.com'
        self.command.config.password = 'password'

        self.command.setup()
        mock_write_config.assert_called_once()

    @patch("nak.command.Config.write_config", autospec=True)
    @patch('builtins.input', autospec=True)
    def test_setup_fill_correct_value_should_call_create_config_and_env_file_correctly(
        self, mock_input, mock_write_config
    ):
        mock_input.side_effect = [
            123456,  # client id
            'test@29next.com',  # email
            'password'  # password
        ]
        with self.assertLogs(level='INFO') as log:
            self.command.setup()

        assert log.output == ['INFO:root:' + LOG_COLOR.SUCCESS.format(
            message='App with client_id 123456 has been setup successfully.')]

        assert mock_write_config.call_count == 1

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
        mock_path_exists.side_effect = [False, False]

        with self.assertRaises(TypeError) as error:
            self.command.build()

        assert str(error.exception) == LOG_COLOR.ERROR.format(
            message=(
                'Unable to locate config or env file. '
                'You can configure config or env file by running "nak setup".'))
        assert mock_zipfile.mock_calls == []

    @patch("os.path.exists")
    @patch("nak.command.zipfile", autospec=True)
    @patch("nak.command.get_all_file", autospec=True)
    @patch("nak.command.Config.write_config", autospec=True)
    def test_build_with_correct_directory_should_create_zip_file_correctly(
        self, mock_write_config, mock_get_file, mock_zipfile, mock_path_exists
    ):

        mock_get_file.return_value = ["test1.file", "test2.file"]
        mock_path_exists.side_effect = [
            # check config dir at build command
            True,
            # check env file at build command
            True
        ]
        with self.assertLogs(level='INFO') as log:
            self.command.build()

        assert mock_zipfile.ZipFile.return_value.mock_calls == [
            call.write('test1.file'),
            call.write('test2.file'),
            call.close(),
        ]
        assert log.output == [
            f"INFO:root:{LOG_COLOR.INFO.format(message='file: test1.file')}",
            f"INFO:root:{LOG_COLOR.INFO.format(message='file: test2.file')}",
            f"INFO:root:{LOG_COLOR.SUCCESS.format(message='Build successfully.')}"
        ]

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
            # check envfile at read_config
            False,
            # check self dir at push command
            False,
        ]

        with self.assertRaises(TypeError) as error:
            self.command.push()

        assert str(error.exception) == LOG_COLOR.ERROR.format(
            message=(
                'Unable to locate config or env file. '
                'You can configure config or env file by running "nak setup".'))

    @patch("builtins.open", autospec=True)
    @patch("os.path.exists", autospec=True)
    @patch("nak.command.get_all_file", autospec=True)
    @patch("nak.command.Config.write_config", autospec=True)
    def test_push_with_failed_on_server_should_log_error_correctly(
        self, mock_write_config, mock_get_file, mock_path_exists, mock_open_file
    ):
        mock_get_file.return_value = ["test1-20200101010101.zip", "test2-20200101010102.zip"]
        mock_path_exists.side_effect = [
            # check envfile at read_config
            True,
            # check self dir at push command
            True
        ]
        self.command.config.client_id = '123456'
        self.command.config.email = 'test@29next.com'

        mock_open_file.return_value = file = MagicMock()
        mock_response = self.mock_gateway.return_value.update_app.return_value
        mock_response.ok = False
        mock_response.json.return_value = {"error": "file size limit"}

        with self.assertLogs(level='INFO') as log:
            self.command.push()

        self.mock_gateway.return_value.update_app.assert_called_once_with(
            files={
                # send with latest file
                'file': ('test2-20200101010102.zip', file)
            }
        )
        assert log.output == [
            f'INFO:root:{LOG_COLOR.INFO.format(message="Pushing to app with client_id 123456")}',
            f'INFO:root:{LOG_COLOR.INFO.format(message="with filename test2-20200101010102.zip")}',
            f'INFO:root:{LOG_COLOR.INFO.format(message="by username test@29next.com")}',
            f"INFO:root:{LOG_COLOR.ERROR.format(message='Upload file to server failed. file size limit')}"
        ]

    @patch("builtins.open", autospec=True)
    @patch("os.path.exists", autospec=True)
    @patch("nak.command.get_all_file", autospec=True)
    @patch("nak.command.Config.write_config", autospec=True)
    def test_push_with_correct_directory_should_call_gateway_correctly(
        self, mock_write_config, mock_get_file, mock_path_exists, mock_open_file
    ):
        mock_get_file.return_value = ["test1-20200101010101.zip", "test2-20200101010102.zip"]
        mock_path_exists.side_effect = [
            # check envfile at read_config
            True,
            # check self dir at push command
            True
        ]
        self.command.config.client_id = '123456'
        self.command.config.email = 'test@29next.com'

        mock_open_file.return_value = file = MagicMock()
        mock_response = self.mock_gateway.return_value.update_app.return_value
        mock_response.ok = True

        with self.assertLogs(level='INFO') as log:
            self.command.push()

        self.mock_gateway.return_value.update_app.assert_called_once_with(
            files={
                # send with latest file
                'file': ('test2-20200101010102.zip', file)
            }
        )
        assert log.output == [
            f'INFO:root:{LOG_COLOR.INFO.format(message="Pushing to app with client_id 123456")}',
            f'INFO:root:{LOG_COLOR.INFO.format(message="with filename test2-20200101010102.zip")}',
            f'INFO:root:{LOG_COLOR.INFO.format(message="by username test@29next.com")}',
            f"INFO:root:{LOG_COLOR.SUCCESS.format(message='Push update file to app successfully.')}"
        ]

    @patch("os.path.exists", autospec=True)
    @patch("nak.command.get_all_file", autospec=True)
    @patch("nak.command.Config.write_config", autospec=True)
    def test_push_with_no_directory_should_raise_error(
        self, mock_write_config, mock_get_file, mock_path_exists
    ):
        mock_get_file.return_value = None
        mock_path_exists.side_effect = [
            # check envfile at read_config
            True,
            # check self dir at push command
            False
        ]

        with self.assertRaises(TypeError) as error:
            self.command.push()

        assert str(error.exception) == LOG_COLOR.ERROR.format(
            message=('No build file available. Run "nak build".'))

    @patch("os.path.exists", autospec=True)
    @patch("nak.command.get_all_file", autospec=True)
    @patch("nak.command.Config.write_config", autospec=True)
    def test_push_with_no_files_in_directory_should_raise_error(
        self, mock_write_config, mock_get_file, mock_path_exists
    ):
        mock_get_file.return_value = None
        mock_path_exists.side_effect = [
            # check envfile at read_config
            True,
            # check self dir at push command
            True
        ]

        with self.assertRaises(TypeError) as error:
            self.command.push()

        assert str(error.exception) == LOG_COLOR.ERROR.format(
            message=('Please run build before push command.'))
