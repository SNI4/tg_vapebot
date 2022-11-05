from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("VAPEBOT_TOKEN")
ADMIN_CHAT_ID = -740976394
