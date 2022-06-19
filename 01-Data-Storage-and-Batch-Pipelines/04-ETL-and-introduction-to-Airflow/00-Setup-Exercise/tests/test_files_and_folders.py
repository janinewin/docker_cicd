import os


def test_files_and_folders():
    expected_folders = ["dags", "data", "logs"]
    current_files_and_folders = os.listdir()

    for expected_folder in expected_folders:
        assert expected_folder in current_files_and_folders
        assert (".gitkeep") in os.listdir(expected_folder)
