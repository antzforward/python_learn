"""
1. for notes, while a empty folder
2. name start with number like 01,for chapter number
3. create md file using folder name,and first line is file name

like AI_for_Humans/I Fundamental Algorithms/01 Introduction to AI
will generate a md file named 01 Introduction to AI and its first line is # 01 Introduction to AI
under the folder.
"""
import os
import pathlib
import subprocess
import re

def main():
    files_dict = {}
    pattern = '^[0-9]+'
    # fd -a -t d ^[0-9]+
    out_text = subprocess.check_output(['fd','-a','-t','d','[0-9]+']).decode('utf-8')
    file_list = ( pathlib.Path(f) for f in out_text.split('\n') if f !='' )
    for filename in file_list:
        if next(os.scandir(filename.resolve()), None):
            continue
        short_name = filename.name
        if re.search( pattern, short_name ):
            files_dict[str(filename.resolve())] = short_name
    for strpath, filename in files_dict.items():
        fullname = pathlib.Path( strpath,f"{filename}.md" )
        if fullname.exists():
            continue
        with fullname.open('w', encoding='utf-8') as f:
            print(f"# {filename}   \n", file=f,end='')##或者用\\\n 都可以的
            print(f"***   \n", file=f, end='')


if __name__ == "__main__":
    main()