import os
import sys


def check_api_key(env_var: str, exit_on_fail: bool = True):
    if env_var not in os.environ:
        print(f"You didn't export {env_var}!!!")
        if exit_on_fail:
            sys.exit(1)
    return True


def get_api_key(env_var):
    return os.environ[env_var] if check_api_key(env_var) else None
