"""
Entry Point for application, running this will run the app
"""

import sys
import argparse
from app.config import dev_cli_choices
from app.factory import create_app


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", choices=dev_cli_choices, default="Dev",
                        help="Config type to use. (Default: Dev)")
    parser.add_argument("-H", "--host", type=str, default="127.0.0.1",
                        help="Web Server Host (Default: 127.0.0.1)")
    parser.add_argument("-p", "--port", type=int, default=8000,
                        help="Web Server Port (Default: 8000)")
    args = parser.parse_args()

    app = create_app(args.config)
    app.run(host=args.host, port=args.port)
