from System_Framework import VirtualTryOnSystem


def main():
    shoe_model_path = "3D_models_assets\shoe_0.obj"  
    system = VirtualTryOnSystem(shoe_model_path)
    system.run()

if __name__ == "__main__":
    main()