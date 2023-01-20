import random

import DiscordRPC
from datetime import datetime


def setup_rpc() -> None:
    """
    Функция инициализирует discord rpc
    """
    try:
        with open("states.txt", "r", encoding="utf-8") as f:
            states = list(map(str.strip, f.readlines()))

        rpc = DiscordRPC.RPC.Set_ID(app_id=1062006362197991454)

        rpc.set_activity(
            details=random.choice(states),
            state=f"Играет с: {datetime.now().strftime('%H:%M')}",
            large_image="logo"
        )
        return rpc
    except Exception as e:
        print(f"RPC error: ({e.__class__})")
