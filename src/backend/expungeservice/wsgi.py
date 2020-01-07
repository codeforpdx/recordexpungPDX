from .app import create_app
import os

tier = os.getenv("TIER", default="development")
application = create_app(tier)

if __name__ == "__main__":
    application.run()
