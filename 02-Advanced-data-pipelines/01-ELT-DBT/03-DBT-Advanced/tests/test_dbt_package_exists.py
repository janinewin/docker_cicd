import os
import pathlib

# current_file = '/home/selim/nico/data-engineering-solutions-week2/02-Advanced-data-pipelines/01-ELT-DBT/01-Setup-DBT/tests/test_dbt_model_documentation.py'
# day_level_dir =  pathlib.Path(os.path.realpath(current_file)).parent.parent.parent


day_level_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent.parent
packages_path = pathlib.Path(os.path.join(day_level_dir, 'dbt_lewagon/packages.yml'))

def test_packages_created():
    assert packages_path.is_file(), "packages.yml has not been created"
