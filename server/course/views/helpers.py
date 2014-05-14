# Helper methods for configuring the setup more easily

ALLOWED_EXTENSIONS = set(["csv"])

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS

def is_valid_year(nr):
    try:
        nr = float(nr)
        if 1900 < nr < 2100: 
            return True
        else:
            return False
    except ValueError:
        return False

