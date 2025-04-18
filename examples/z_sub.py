
import time

import zenoh


def main(conf: zenoh.Config, key: str):
    # initiate logging
    zenoh.init_log_from_env_or("error")

    print("Opening session...")
    with zenoh.open(conf) as session:

        print(f"Declaring Subscriber on '{key}'...")

        def listener(sample: zenoh.Sample):
            try:
                # 尝试将负载转换为 UTF-8 字符串
                payload_str = sample.payload.to_string()
                print(f">> [Subscriber] Received {sample.kind} ('{sample.key_expr}': '{payload_str}')")
            except ValueError:
                # 如果不是 UTF-8 数据，则显示二进制表示
                payload_bytes = sample.payload.to_bytes()
                print(f">> [Subscriber] Received {sample.kind} ('{sample.key_expr}': <二进制数据，长度: {len(payload_bytes)} 字节>)")
                # 可选：显示数据的十六进制表示
                print(f"   十六进制: {payload_bytes.hex()[:100]}{'...' if len(payload_bytes) > 50 else ''}")

        session.declare_subscriber(key, listener)

        print("Press CTRL-C to quit...")
        while True:
            time.sleep(1)


# --- Command line argument parsing --- --- --- --- --- ---
if __name__ == "__main__":
    import argparse
    import json

    import common

    parser = argparse.ArgumentParser(prog="z_sub", description="zenoh sub example")
    common.add_config_arguments(parser)
    parser.add_argument(
        "--key",
        "-k",
        dest="key",
        # default="**",
        # default="v1/api/routing/state",
        # default="v1/vehicle/status/control_mode",
        # default="v1/api/vehicle/command/acceleration",
        default="**/acceleration",
        type=str,
        help="The key expression to subscribe to.",
    )

    args = parser.parse_args()
    conf = common.get_config_from_args(args)

    main(conf, args.key)
