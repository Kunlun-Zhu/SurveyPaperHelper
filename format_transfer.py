from tqdm import tqdm
import re
from typing import List

def bibtex_to_formatted_text(bibtex):
    # Extracting the BibTeX type and content
    entry_type_match = re.match(r'@(\w+){', bibtex)
    entry_type = entry_type_match.group(1) if entry_type_match else None

    # Dictionary to store BibTeX key-value pairs
    bibtex_dict = {}

    # Regex to find key-value pairs in the BibTeX entry
    for key, value in re.findall(r'\s(\w+)\s*=\s*{([^}]+)}', bibtex):
        bibtex_dict[key.lower()] = value.strip()

    # Building the formatted text based on entry type
    formatted_text = ""
    if entry_type:
        # Common fields
        title = bibtex_dict.get('title', 'No title').replace("{", "").replace("}", "")
        authors = bibtex_dict.get('author', 'No author').replace(" and ", ", ").replace("{", "").replace("}", "")
        year = bibtex_dict.get('year', 'No year')

        if entry_type == 'book':
            publisher = bibtex_dict.get('publisher', 'No publisher')
            url = bibtex_dict.get('url', None)
            url_text = f" [Link]({url})" if url else ""
            formatted_text = f"**{title}** *{authors}.* {publisher}, {year}.{url_text}"
        
        elif entry_type == 'misc':
            howpublished = bibtex_dict.get('howpublished', 'No source')
            eprint = bibtex_dict.get('eprint', 'No eprint ID')
            archive_prefix = bibtex_dict.get('archiveprefix', 'No archive prefix')
            primary_class = bibtex_dict.get('primaryclass', 'No primary class')
            formatted_text = f"**{title}** *{authors}.* arXiv {year}. [[abs](https://arxiv.org/abs/{eprint})]"
        
        elif entry_type == 'article':
            journal = bibtex_dict.get('journal', 'No journal').replace("{", "").replace("}", "")
            if "arXiv" in journal:
                eprint = bibtex_dict.get('eprint', bibtex_dict.get('journal').split(':')[-1])
                formatted_text = f"**{title}** *{authors}.* arXiv preprint arXiv:{eprint}, {year}. [[abs](https://arxiv.org/abs/{eprint})]"
            else:
                formatted_text = f"**{title}** *{authors}.* {journal}, {year}."
        
        elif entry_type == 'inproceedings':
            conference = bibtex_dict.get('booktitle', 'No conference').replace("{", "").replace("}", "")
            url = bibtex_dict.get('url', "No URL")
            formatted_text = f"**{title}** *{authors}.* Presented at {conference}, {year}. [Link]({url})"
        
    return formatted_text


def read_bibtex_file(bibtex_file_path: str) -> List[str]:
    """从BibTeX文件中读取所有内容。"""
    with open(bibtex_file_path, 'r', encoding='utf-8') as file:
        return file.read()

def find_bibtex_entries(bibtex_content: str) -> List[str]:
    """从给定的 BibTeX 字符串中提取所有条目。"""
    entries = []
    # 正则表达式匹配 BibTeX 条目，确保匹配到完整的条目
    # 这里使用非贪婪匹配 .*? 确保只匹配到第一个闭大括号，并且使用 re.DOTALL 以匹配换行符
    pattern = re.compile(r'(@\w+\s*{[^}]*?,.*?)}\s*}', re.DOTALL)
    matches = pattern.finditer(bibtex_content)
    for match in matches:
        entries.append(match.group(0))
    return entries


# 转换文件
if __name__ == '__main__':

    bibtex_file_path = './cited.txt'
    bibtex_content = read_bibtex_file(bibtex_file_path)
    entries = find_bibtex_entries(bibtex_content)
    print(entries)
    output_file = './cited_markdown.txt'

    with open(output_file, 'w', encoding='utf-8') as file:
        id = 1
        for entry in tqdm(entries):
            response = bibtex_to_formatted_text(entry).strip()
            file.write(str(id) + '. '+ response + '\n')
            id += 1