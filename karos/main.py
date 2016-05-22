'''
Main application launcher

This script can be called via 'python main.py', and is also linked via setuptool's console_script entry point

'''
from core.main import KarosApp

def run():
    app = KarosApp().run()

'''App is being run as python core/main.py. Run the app'''
if __name__ == '__main__':
    run()

