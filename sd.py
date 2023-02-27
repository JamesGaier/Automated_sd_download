from os import chdir
from pathlib import Path
import urllib.request
from subprocess import Popen, PIPE
from sys import exit

# models
class Model:
    def __init__(self, name, url):
        self.name = name
        self.url = url

def start_process(cmd, blocking=True):
    process = Popen(cmd, shell=True)
    if blocking:
        process.wait()
    return process

# Print the models that the user can download and use with the Stable-diffusion gui
def print_user_input(models):
    print("Hey guys!  This is an installer for Stable-diffusion.")
    print("Select the model you want to use: ")
    for num, model in enumerate(models):
        print(f"{num + 1}. {model.name}")

# Load models
def make_models():
    names = [
        "sd-v1-4.ckpt", 
        "sd-v1-4-full-ema.ckpt", 
        "512-base-ema.ckpt", 
        "v2-1_768-ema-pruned.ckpt", 
        "ProtoGen_X5.8.ckpt"
    ]
    urls = [
        "https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt",
        "https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4-full-ema.ckpt",
        "https://huggingface.co/stabilityai/stable-diffusion-2-base/resolve/main/512-base-ema.ckpt",
        "https://huggingface.co/stabilityai/stable-diffusion-2-1/resolve/main/v2-1_768-ema-pruned.ckpt",
        "https://huggingface.co/darkstorm2150/Protogen_x5.8_Official_Release/resolve/main/ProtoGen_X5.8.ckpt"
    ] 
    return list(map(  lambda name,url: Model(name, url), names, urls))

# generic function for getting user input
def get_numeric_input(max_num):
    # Check if the user input is a number
    result = input()
    if not result.isnumeric():
        print(f"You did not enter a number {result}, please enter a number.")
        get_numeric_input(max_num)

    # Check if the number that was entered is a valid choice
    num_result = int(result)
    if num_result > max_num:
        print(f"You entered {num_result}, a number that is not in the list.")
        result = input()
        num_result = int(result)
        get_numeric_input(max_num)

    return num_result - 1

def file_exists(file_name):
    path = Path(f"stable-diffusion-webui\models\Stable-diffusion\{file_name}")
    return path.is_file()

def get_model_input(models):
    # fetch the model
    user_choice = get_numeric_input(len(models))
    file_name = models[user_choice].name
    file_present = file_exists(file_name)

    # check if the model is already in the models folder
    if file_present:
        print("Model already downloaded.")
        return

    # download if the model is not in the models folder
    print("DOWNLOADING PLEASE WAIT....")
    model_path = f"stable-diffusion-webui/models/Stable-diffusion/{file_name}" 
    urllib.request.urlretrieve(models[user_choice].url, model_path)

def print_settings_prompt():
    print("I reccomend that you use low/medium video ram if you have older than a 30 series graphics card")
    print("Otherwise, you don't need to toggle low/medium video ram")
    print("Please choose a vram usage")
    print("1. low")
    print("2. medium")
    print("3. high")

def get_settings_input():
    num_settings = 3
    user_choice = get_numeric_input(num_settings)
    vram_args = ["--lowvram", "--medvram", ""]
    return vram_args[user_choice]

def main():
    # Clone the git repo into your directory
    stable_diffusion_ui = "https://github.com/AUTOMATIC1111/stable-diffusion-webui.git"
    start_process(['git', 'clone', stable_diffusion_ui])

    # Get the model which the webui will be using
    models = make_models() 
    print_user_input(models)
    get_model_input(models)

    # Ask user what settings they want for ai
    print_settings_prompt()
    vram_choice = get_settings_input()
    
    # run stable diffusion web-ui
    chdir("stable-diffusion-webui")
    start_process(["webui.bat", "--xformers", "--opt-split-attention", vram_choice])

if __name__ == "__main__":
    main()
