from src import TELEGRAM_API_TOKEN
from src.telegram import get_chat_id, get_update_data
from pprint import pprint

if __name__ == "__main__":
    pprint(get_update_data(TELEGRAM_API_TOKEN))
