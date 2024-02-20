from dataclasses import dataclass

@dataclass
class File:
    id: int
    name: str
    categories: list[str]
    parent: int
    size: int


"""
Task 1
"""

# Implement depth-first search recursively
def depthFirstSearch(file: File, par_dict: dict, leaves: list[File]) -> File:
    # Check if the file is a parent
    if file.id in par_dict.keys():
        # If it is, call DFS on all child files
        for i in range(len(par_dict[file.id])):
            depthFirstSearch(par_dict[file.id][i], par_dict, leaves)
    # Otherwise, add it to the list of leaves
    else:
        leaves.append(file.name)

    # DEBUG
    # print(leaves)
    return leaves


def leafFiles(files: list[File]) -> list[str]:
    leaves = []
    roots = []
    parent_dict = {}

    for file in files:
        # Find all of the root files in the test files
        if file.parent == -1:
            roots.append(file)
        # Adds the file ID to the list if the parent ID is already a key in the dict
        elif file.parent in parent_dict.keys():
            parent_dict[file.parent].append(file)
        # Otherwise, creates a new list containing the file ID
        else:
            parent_dict[file.parent] = [file]

    # DEBUG
    # print(roots)
    # print(parent_dict)

    # Implement depth-first search on all root files
    # Assumes that there are no infinite branches in the directory
    for file in roots:
        for name in depthFirstSearch(file, parent_dict, leaves=[]):
            # Only adds non-duplicate file names to the list
            if name not in leaves:
                leaves.append(name)

    # final debug check
    # print(sorted(leaves))
    return leaves


"""
Task 2
"""
def kLargestCategories(files: list[File], k: int) -> list[str]:
    # Create a dictionary to store all the categories
    category_dict = {}

    # Count the number of files in each category
    for file in files:
        for category in file.categories:
            # If the category is already in the dictionary, add one to the value
            if category in category_dict.keys():
                category_dict[category] += 1
            # Otherwise, create a new key-value pair, with the value set to one
            else:
                category_dict[category] = 1

    # Sort the list of categories, first by size (descending), then alphabetically (ascending)
    sorted_category = sorted(category_dict.keys(), key = lambda x: (-category_dict[x], x))

    # DEBUG
    # print(category_dict)
    # print(sorted_category)
    # print(sorted_category[0:k])

    return sorted_category[0:k]


"""
Task 3
"""
# Implement depth-first search recursively, storing the size
def depthFirstSize(file: File, par_dict: dict) -> int:
    file_size: int = file.size

    # DEBUG
    # print(f"> id: {file.id} | size: {file.size} | total: {file_size}")

    # Check if the file is a parent
    if file.id in par_dict.keys():
        # If it is, call DFS on all child files
        for i in range(len(par_dict[file.id])):

            # DEBUG
            # print(par_dict[file.id][i].id)
            file_size += depthFirstSize(par_dict[file.id][i], par_dict)
    else:
        return file_size
    
    # I forgot to return the file size so it would return NoneType
    # for anything deeper than the second level of recursion (ie. Folder2)
    return file_size


def largestFileSize(files: list[File]) -> int:
    roots = []
    parent_dict = {}
    file_sizes = []

    for file in files:
        # Find all of the root files in the test files
        if file.parent == -1:
            roots.append(file)
        # Adds the file ID to the list if the parent ID is already a key in the dict
        elif file.parent in parent_dict.keys():
            parent_dict[file.parent].append(file)
        # Otherwise, creates a new list containing the file ID
        else:
            parent_dict[file.parent] = [file]

    # DEBUG
    # print(parent_dict)
    # print(roots)

    # For the purposes of this question, we can actually optimise by only checking root files.
    # This is because any child files have to be equal to or less than the size of the parent file.
    # This also assumes that folders are counted as files, and is probably not practical in a real use case.
            
    for file in roots:
        file_sizes.append(depthFirstSize(file, parent_dict))

    # DEBUG
    # print(file_sizes)
    
    return max(file_sizes)


if __name__ == '__main__':
    testFiles = [
        File(1, "Document.txt", ["Documents"], 3, 1024),
        File(2, "Image.jpg", ["Media", "Photos"], 34, 2048),
        File(3, "Folder", ["Folder"], -1, 0),
        File(5, "Spreadsheet.xlsx", ["Documents", "Excel"], 3, 4096),
        File(8, "Backup.zip", ["Backup"], 233, 8192),
        File(13, "Presentation.pptx", ["Documents", "Presentation"], 3, 3072),
        File(21, "Video.mp4", ["Media", "Videos"], 34, 6144),
        File(34, "Folder2", ["Folder"], 3, 0),
        File(55, "Code.py", ["Programming"], -1, 1536),
        File(89, "Audio.mp3", ["Media", "Audio"], 34, 2560),
        File(144, "Spreadsheet2.xlsx", ["Documents", "Excel"], 3, 2048),
        File(233, "Folder3", ["Folder"], -1, 4096),
    ]

    assert sorted(leafFiles(testFiles)) == [
        "Audio.mp3",
        "Backup.zip",
        "Code.py",
        "Document.txt",
        "Image.jpg",
        "Presentation.pptx",
        "Spreadsheet.xlsx",
        "Spreadsheet2.xlsx",
        "Video.mp4"
    ]

    assert kLargestCategories(testFiles, 3) == [
        "Documents", "Folder", "Media"
    ]

    assert largestFileSize(testFiles) == 20992
