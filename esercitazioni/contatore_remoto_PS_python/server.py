from counterSkeleton import CounterSkeleton
from serverImpl import serverImpl

def main():
    impl = serverImpl()
    skeleton = CounterSkeleton(impl)
    skeleton.run_function()


if __name__ == "__main__":
    main()