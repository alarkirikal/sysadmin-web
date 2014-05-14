# Helper methods for configuring the setup more easily

ALLOWED_EXTENSIONS = set(["csv"])

def allowed_file(filename):
    """ Function to check the file type

    Args:
        filename (str): name of the file being checked

    Returns:
        boolean. If the file name is allowed or not

    """

    return "." in filename and \
        filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


def is_valid_year(nr):
    """ Function to check, whether the number being checked is a valid year
    
    Args:
        nr (int): Number to check

    Returns:
        boolean. If the number is a valid year

    """

    try:
        # Convert the number to be sure
        nr = float(nr)
        if 1900 < nr < 2100: 
            return True
        else:
            return False
    except ValueError:
        return False

