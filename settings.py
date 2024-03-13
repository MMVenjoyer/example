from envparse import Env
env = Env()

TOKEN = "6805485184:AAF2Dau5aElXIqfxiGpyVqviwYeHaYm7DZo"
REAL_DATABASE_URL = env.str("REAL_DATABASE_URL", default="postgresql://postgres:root@127.0.0.1:5432/db_for_tz")