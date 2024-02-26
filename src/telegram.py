import requests


def get_chat_id(api_token):
    # 發送 getUpdates 請求獲取最新的更新
    response = requests.get(f"https://api.telegram.org/bot{api_token}/getUpdates")

    # 解析 API 响應，提取聊天 ID
    if response.status_code == 200:
        data = response.json()
        if "result" in data and data["result"]:
            chat_id = data["result"][0]["message"]["chat"]["id"]
            return chat_id
    return None


def get_update_data(api_token):
    response = requests.get(f"https://api.telegram.org/bot{api_token}/getUpdates")
    if response.status_code == 200:
        data = response.json()
        return data
    return None


if __name__ == "__main__":
    api_token = "YOUR_API_TOKEN"

    # 獲取聊天 ID
    chat_id = get_chat_id(api_token)
    if chat_id:
        print(f"聊天 ID: {chat_id}")
    else:
        print("獲取聊天 ID 失敗。")
