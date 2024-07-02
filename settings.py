from dotenv import load_dotenv
import os

load_dotenv()

MITMPROXY = os.environ["MITMPROXY"]
MITMPROXY_PORT= int(os.environ.get("MITMPROXY_PORT", 8080))
OSU_PATH = os.environ["OSU_PATH"]

CLOUDFLARE = os.environ["CLOUDFLARE"]

DEVELOPER = os.environ["DEVELOPER"]
SQLLITE_FILE_NAME = os.environ["SQLLITE_FILE_NAME"]
