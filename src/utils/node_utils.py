import asyncio

def read_config_file(config_file_path):
    """Reads the config file and returns the config dictionary.

    Args:
        config_file_path: Path to the config file.

    Returns:
        List of tuples containing the ip and port of the bootstrap nodes.
    """
    with open(config_file_path, 'r') as config_file:
        config = config_file.readlines()

    return [{'ip' : ip, 'port' : int(port.replace('\n', ''))} for ip, port in [tuple(line.split(' ')) for line in config]]

def run_in_loop(function, loop):
    """
    Runs a function in the given loop.
    """
    return asyncio.run_coroutine_threadsafe(function, loop)