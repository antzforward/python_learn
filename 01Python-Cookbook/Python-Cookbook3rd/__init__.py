import sys
import os
chapters = [
    '01 Data Structures and Algorithms',
    '02 Strings and Text',
    '03 Numbers,Dates, and Times',
    '04 Iterators and Generators',
    '05 Files and IO',
    '06 Data Encoding and Processing',
    '07 Functions',
    '08 Classes and Objects',
    '09 MetaProgramming',
    '10 Modules and Packages',
    '11 Network and Web Programming',
    '12 Concurrency',
    '13 Utility Scripting and System Administration',
    '14 Testing,Debugging,and Exceptions',
    '15 C Extensions'
]
cur = os.getcwd()
for chapter in chapters:
    chapter_path = os.path.join(cur, chapter);
    if chapter_path not in sys.path:
        sys.path.append( chapter_path )
