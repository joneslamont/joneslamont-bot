from src.core.rust_bridge import jl_ping


def main() -> None:
    print("JonesLamont Bot boot sequence OK")
    print("RUST:", jl_ping())


if __name__ == "__main__":
    main()

