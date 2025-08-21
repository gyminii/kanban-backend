try:
    import strawberry
    print("Strawberry imported successfully!")
    print(f"Strawberry version: {strawberry.__version__}")
    print(f"Location: {strawberry.__file__}")
except ImportError as e:
    print(f"Import error: {e}")