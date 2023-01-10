import DiscordRPC
import time


def setup():
    rpc = DiscordRPC.RPC.Set_ID(app_id=1062006362197991454)

    rpc.set_activity(
        state="pip install discord-rpc",
        details="Discord RPC"
    )
