from rho import __version__
from rho import mpl_setup


def test_version():
    assert __version__ == "0.1.0"


def test_mpl_setup():
    cs = mpl_setup(True)
    assert len(cs) == 10

    cs = mpl_setup(False)
    assert len(cs) == 10


if __name__ == "__main__":
    test_mpl_setup()
    print("Done")
