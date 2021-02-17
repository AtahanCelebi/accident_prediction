import os
def count_png():
    c =0
    print(os.getcwd())
    path = os.getcwd()
    all_files = os.listdir(path)
    for file in all_files:
        if file.endswith(".png"):
            c +=1

    return c
def delete_png():
    path = os.getcwd()
    all_files = os.listdir(path)
    for file in all_files:
        if file.endswith(".png"):
            os.remove(file)

    print("All .png files deleted in the directory")
delete_png()