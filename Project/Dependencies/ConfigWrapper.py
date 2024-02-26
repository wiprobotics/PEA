import configparser


class Config():
    """This is a class to handle the config file for the project.

        Args:
            filepath (_string_): The path to the config file.

        Functions:
            get : This function gets a string from the config file.
            get_int : This function gets an integer from the config file.
            get_float : This function gets a float from the config file.
            get_boolean : This function gets a boolean from the config file.
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.config = configparser.ConfigParser()
        self.config.read(self.filepath)

    def get(self, section, option):
        """This function gets a string from the config file.

        Args:
            section (_string_): The header section of the config file.
            option (_string_): The option to be retrieved from the config file.

        Returns:
            _string_: The value of the option in the config file.
        """
        return self.config.get(section, option)

    def get_int(self, section, option):
        """This function gets an integer from the config file.

        Args:
            section (_string_): The header section of the config file.
            option (_string_): The option to be retrieved from the config file.

        Returns:
            _int_: The value of the option in the config file.
        """
        return self.config.getint(section, option)

    def get_float(self, section, option):
        """This function gets a float from the config file.

        Args:
            section (_string_): The header section of the config file.
            option (_string_): The option to be retrieved from the config file.

        Returns:
            _float_: The value of the option in the config file.
        """
        return self.config.getfloat(section, option)

    def get_boolean(self, section, option):
        """This function gets a boolean from the config file.

        Args:
            section (_string_): The header section of the config file.
            option (_string_): The option to be retrieved from the config file.

        Returns:
            _bool_: The value of the option in the config file.
        """
        return self.config.getboolean(section, option)
