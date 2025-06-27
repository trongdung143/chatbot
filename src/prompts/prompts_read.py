def read_prompt(file_path: str = "src/prompts/prompts.txt"):
    with open(file_path, "r") as file:
        content = file.read()
    return content
