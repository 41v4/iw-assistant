if __name__ == "__main__":
    import uvicorn

    kwargs = {"host": "0.0.0.0", "port": 8000}

    kwargs.update({"reload": True, "reload_includes": [".env"]})

    uvicorn.run("app.main:app", **kwargs)
