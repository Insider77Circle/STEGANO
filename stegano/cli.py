"""STEGANO command-line interface."""

from __future__ import annotations

import argparse
import json
import sys

from stegano import channels
from stegano.detector import report as detect_report
from stegano.sanitizer import strip as sanitize_strip


def cmd_list(_args: argparse.Namespace) -> int:
    for name in channels.names():
        ch = channels.get(name)
        print(f"{name:20s} {ch.description}")
    return 0


def cmd_encode(args: argparse.Namespace) -> int:
    ch = channels.get(args.channel)
    encoded = ch.encode(args.payload)
    out = channels.embed(args.carrier, encoded, args.position) if args.carrier else encoded
    if args.repr:
        print(repr(out))
    else:
        sys.stdout.write(out)
    return 0


def cmd_decode(args: argparse.Namespace) -> int:
    ch = channels.get(args.channel)
    text = args.text if args.text is not None else sys.stdin.read()
    print(ch.decode(text))
    return 0


def cmd_detect(args: argparse.Namespace) -> int:
    text = args.text if args.text is not None else sys.stdin.read()
    print(json.dumps(detect_report(text), indent=2))
    return 0


def cmd_sanitize(args: argparse.Namespace) -> int:
    text = args.text if args.text is not None else sys.stdin.read()
    sys.stdout.write(sanitize_strip(text))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="stegano",
                                     description="Invisible-Unicode steganography toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list", help="list channels"); p.set_defaults(func=cmd_list)

    p = sub.add_parser("encode", help="encode a payload")
    p.add_argument("--channel", required=True, choices=channels.names())
    p.add_argument("--payload", required=True)
    p.add_argument("--carrier", default=None)
    p.add_argument("--position", default="middle")
    p.add_argument("--repr", action="store_true")
    p.set_defaults(func=cmd_encode)

    p = sub.add_parser("decode", help="decode a payload")
    p.add_argument("--channel", required=True, choices=channels.names())
    p.add_argument("--text", default=None)
    p.set_defaults(func=cmd_decode)

    p = sub.add_parser("detect", help="scan text for hidden content")
    p.add_argument("--text", default=None)
    p.set_defaults(func=cmd_detect)

    p = sub.add_parser("sanitize", help="strip invisible characters")
    p.add_argument("--text", default=None)
    p.set_defaults(func=cmd_sanitize)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
