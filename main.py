if __name__ == "__main__":
    # import asyncio
    # import hypercorn
    # from hypercorn.asyncio import serve
    # from hypercorn.config import Config
    # from app import app
    import uvicorn

    # class CustomConfig(Config):
    #     use_reloader = True
    uvicorn.run("index:app", host="0.0.0.0", port=8000, workers=2)