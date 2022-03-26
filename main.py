import fixmac # no qa
from game import Game
import argparse

def main():
    parser = argparse.ArgumentParser(description='Solar system in 3d')
    parser.add_argument("--fullscreen", "-f", action="store_true", default=False, help="Start in fullscreen")
    parser.add_argument("--size_x", "-sx", type=int, default=800, help="Resolution (X)")
    parser.add_argument("--size_y", "-sy", type=int, default=600, help="Resolution (Y)")
    parser.add_argument("--speed", "-s", type=float, default=1, help="Resolution (Y)")
    args = parser.parse_args()
    # Start the game
    game = Game(fullscreen=args.fullscreen, size_x=args.size_x, size_y=args.size_y, speed=args.speed)
    game.run()

if __name__ == "__main__":
    main()
