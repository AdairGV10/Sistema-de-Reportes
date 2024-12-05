try:
    import core
    print("¡Importación de 'core' exitosa!")
except ModuleNotFoundError as e:
    print(f"Error al importar 'core': {e}")