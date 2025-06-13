import os
from langchain_core.tools import tool
import shutil
import glob


@tool
def save_upload_file(file_name: str, new_file_name: str = None) -> str:
    """
    Save a file for the user, optionally with a new name, while preserving the extension of the old file.

    Args:
        file_name (str): The original file name located in the temporary folder 'src/agents/data/temp/'.
        new_file_name (str, optional): The new name to save the file under in 'src/data/'.
                                    If not provided, the original name will be used.

    Returns:
        str: Message indicating the result of the save operation.
    """
    try:
        temp_path = f"src/agents/data/temp/{file_name}"
        save_dir = "src/data"

        if not os.path.exists(temp_path):
            return "File does not exist in the temporary folder."

        os.makedirs(save_dir, exist_ok=True)

        target_name = new_file_name if new_file_name else file_name
        target_path = os.path.join(save_dir, target_name)

        if os.path.exists(target_path):
            return "A file with the new name already exists."

        shutil.move(temp_path, target_path)
        return f"File has been successfully saved as {target_name}."

    except Exception as e:
        return f"Error while saving the file: {str(e)}"


@tool
def show_saved_file_folder() -> str:
    """
    Show all files saved in a specified folder.

    Returns:
        str: A list of all files in the folder or a message if it's empty.
    """
    try:
        folder_path = "src/data"
        files = glob.glob(f"{folder_path}/*")
        if not files:
            return "The folder is empty."

        list_file = "File list:\n"
        for file in files:
            list_file += "• " + os.path.basename(file) + "\n"
        return list_file

    except Exception as e:
        return f"Error while listing files: {str(e)}"


@tool
def remove_file(file_name: str) -> str:
    """
    Delete a specific file from a given folder.

    Args:
        file_name (str): The name of the file to delete.

    Returns:
        str: Message indicating whether the file was successfully deleted.
    """
    try:
        folder_path = "src/data"
        file_path = os.path.join(folder_path, file_name)
        if not os.path.exists(file_path):
            return "File not found in the folder."

        os.remove(file_path)
        return f"{file_name} has been deleted."

    except Exception as e:
        return f"Error while deleting the file: {str(e)}"


@tool
def rename_file(file_name: str, new_file_name: str) -> str:
    """
    Rename a file in the specified folder.

    Args:
        file_name (str): The current name of the file.
        new_file_name (str): The new name to assign to the file.

    Returns:
        str: Message indicating the result of the rename operation.
    """
    try:
        folder_path = "src/data"
        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(folder_path, new_file_name)

        if not os.path.exists(old_path):
            return "Original file does not exist."

        if os.path.exists(new_path):
            return "A file with the new name already exists."

        os.rename(old_path, new_path)
        return f"Renamed file {file_name} to {new_file_name}."

    except Exception as e:
        return f"Error while renaming the file: {str(e)}"


@tool
def write_note(note_content: str, notefile_name: str) -> str:
    """
    Create or overwrite a note file.

    Args:
        note_content (str): The content of the note.
        notefile_name (str): The file name to save the note as, inside 'src/data/'.

    Returns:
        str: Confirmation message.
    """
    try:
        folder_path = "src/data"
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, notefile_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(note_content)
        return "Note has been saved."

    except Exception as e:
        return f"Error while writing note: {str(e)}"


@tool
def read_note(notefile_name: str) -> str:
    """
    Read the content from a note file.

    Args:
        notefile_name (str): The name of the note file located in 'src/data'.

    Returns:
        str: The note content or an error message if not found.
    """
    try:
        folder_path = "src/data"
        file_path = os.path.join(folder_path, notefile_name)

        if not os.path.exists(file_path):
            return f"Note {notefile_name} not found in the notes folder."

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return f"Note content:\n{content}"

    except Exception as e:
        return f"Error while reading note: {str(e)}"


@tool
def download_file(file_name: str) -> str:
    """
    Generate a link to download the file.

    Args:
        file_name (str): The name of the file need download'.

    Returns:
        str: A message containing a download link.
    """
    try:
        file_path = f"src/data/{file_name}"
        if os.path.exists(file_path):
            return f"You can download the file at the following link: [download/{file_name}]."
        else:
            return f"File {file_name} not found."

    except Exception as e:
        return f"Error while generating download link: {str(e)}"
