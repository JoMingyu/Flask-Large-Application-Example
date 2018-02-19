import unittest as ut

from app import app

if __name__ == '__main__':
    app.testing = True

    all_tests = ut.TestLoader().discover('tests', '*.py')
    ut.TextTestRunner().run(all_tests)
