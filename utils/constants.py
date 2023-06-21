from pathlib import Path
cwd = Path.cwd()

# DATABASE_PATH = cwd.parent.parent / "database"
SCALE_PERCENT = 10
FR_MODEL = 'large'

# FIRST_PENALTY = 50000
# REMAINING_PENALTY = 10000

FR_TOLERANCE = 0.49

CAP_PROP_FRAME_WIDTH = 1920
CAP_PROP_FRAME_HEIGHT = 1080

FREEZE_TIME_OF_CAUGHT_KNOWN_FACE = 2

ATTENDANCE_FREEZE_TIME = 30*60

ATTENDANCE_EXPIRATION_TIME = 60*60*15

POSTGRESQL_URL = 'postgresql+psycopg2://login:password@localhost:5432/attendance'

# Image_Main_Path = cwd / "static"/ "temp"

# DATABASE_Main_Path = cwd / "static"/ "database"

UNKNOWN_FACE_TEXT = 'MA`LUMOT TOPILMADI'

WEEKS_NAME = ['mon', 'tue', 'wen', 'thu', 'fre', 'sat', 'sun']
