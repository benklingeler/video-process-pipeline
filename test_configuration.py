from lib.configuration import loadConfiguration, saveConfiguration


def test_saveAndLoadConfiguration():
    """
    Test cases for the saveConfiguration and loadConfiguration functions.

    - Test loading configuration: Asserts that the loadConfiguration function returns True, indicating successful loading of the configuration.
    - Test saving configuration: Asserts that the saveConfiguration function returns True, indicating successful saving of the configuration.
    """
    assert loadConfiguration() == True
    assert saveConfiguration() == True
