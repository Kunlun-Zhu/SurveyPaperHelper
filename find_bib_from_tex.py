import re
from typing import List

def extract_citations(latex_content: str) -> List[str]:
    """从LaTeX文本中提取所有的引用键（cite keys）。"""
    # 匹配 \cite{key1,key2,...} 以及 \citep{} 和 \citet{}
    citations = re.findall(r'\\cite[t|p]?{([^}]+)}', latex_content)
    # 将所有引用分割并去重
    citation_list = list(set([key.strip() for citation in citations for key in citation.split(',')]))
    return citation_list

def read_bibtex_file(bibtex_file_path: str) -> List[str]:
    """从BibTeX文件中读取所有内容。"""
    with open(bibtex_file_path, 'r', encoding='utf-8') as file:
        return file.read()

def find_bibtex_entries(citation_keys: List[str], bibtex_content: str) -> List[str]:
    """根据引用键在BibTeX内容中找到相应的条目。"""
    entries = []
    for key in citation_keys:
        # 正则表达式匹配 BibTeX 条目，确保匹配到完整的条目
        pattern = re.compile(r'(@\w+\s*{\s*' + re.escape(key) + r'\s*,.*?)}\s*}', re.DOTALL)
        match = pattern.search(bibtex_content)
        if match:
            entries.append(match.group(0))
    return entries

def sort_entries_by_year(entries: List[str]) -> List[str]:
    """Sort BibTeX entries by year, putting entries without a year at the beginning."""
    entries_with_year = []
    for entry in entries:
        # Match the year, handling spaces and different braces/quotes
        year_match = re.search(r'year\s*=\s*[{"](\d{4})[}"]', entry)
        if year_match:
            year = int(year_match.group(1))
        else:
            year = 0  # Default year for entries without a year specified
            print(f"No year found, assigning default year 0: {entry}")  # Optional: for debugging

        # Append the entry with its year (default or actual)
        entries_with_year.append((year, entry))
    
    # Sort by year
    sorted_entries = sorted(entries_with_year, key=lambda x: x[0])
    
    # Return only the entries, sorted by year
    return [entry[1] for entry in sorted_entries]

def process_citations(latex_content: str, bibtex_file_path: str) -> List[str]:
    """处理LaTeX文本和BibTeX文件，返回排序后的被引用的BibTeX条目列表。"""
    # 提取引用
    citation_keys = extract_citations(latex_content)
    #print("citation_keys:", citation_keys)
    # 读取BibTeX文件内容
    bibtex_content = read_bibtex_file(bibtex_file_path)
    #print("bibtex_content:", bibtex_content)
    # 查找对应的BibTeX条目
    entries = find_bibtex_entries(citation_keys, bibtex_content)
    #print("entries:", entries)
    # 按年份排序条目
    sorted_entries = sort_entries_by_year(entries)
    #print("sorted_entries:", sorted_entries)
    return sorted_entries

# 示例使用

if __name__ == '__main__':
    
    latex_content = """
    The development of artificial intelligence (AI) has revolutionized human society thanks to their powerful capabilities in many aspects, such as visual perception \citep{alayrac2022flamingo,li2023silkie}, language understanding \citep{wei2021finetuned,schick2023toolformer}, reasoning optimization \citep{wei2022chain,hao2023reasoning,hu2023language}, etc.  For example, the launch of AlphaFold \citep{jumper2021highly} by DeepMind in 2020 significantly revolutionized the field of protein structure prediction. This AI-driven technology provided unprecedented accuracy in determining the 3D shapes of proteins, a task that previously required extensive time and resources. This innovation not only minimized computational costs but also accelerated scientific research, facilitating breakthroughs in understanding diseases like Alzheimer's and contributing to the development of new medications, thereby enhancing the potential for patient treatment and advancing the frontiers of biological research. 

    However, the development of AI is not a smooth journey. Early AI research was mainly developed from the 1950s to the 1970s. AI during this period mainly focuses on symbolic research \citep{stryker1959symbolic,turner1975symbolic} and connectionism \citep{buckner1997connectionism,medler1998brief}, which lays the groundwork for computational approaches to intelligence. From the 1980s to the 1990s, AI faces its winter, and many researchers shift to practical applications due to high expectations and subsequent disappointments of its development. The rise of machine learning and neural networks \citep{zadeh1996fuzzy,kosko1992neural} from the 1990s to the 2010s brings hope to researchers, which leads to significant improvements in various applications like natural language processing, computer vision, and analytics. Starting from the 2010s, the advent of deep learning technologies revolutionized AI capabilities, with significant breakthroughs in image \citep{lu2007survey,rawat2017deep} and speech recognition \citep{gaikwad2010review,povey2011kaldi}. In recent years, with the emergence of ChatGPT \citep{wu2023brief,zhong2023can}, the popularity of large language model (LLM) has also transformed AI research due to its superior reasoning and planning capabilities.  

    Although AI has brought huge improvements to human society, the increasing material and spiritual demands of society have rendered people discontent with the mere convenience provided by AI. Consequently, achieving Artificial General Intelligence (AGI) that enables AI to perform a wider range of tasks more efficiently and effectively has emerged as a pressing concern, which used to describe an AI system that is at least as capable as a human at most tasks \citep{wang2018conceptions,voss2023concepts}.  Therefore, our paper aims to raise attention to the pressing research question: \textit{how far are we from AGI and how can we get to it?}

    To investigate this question, existing research mainly falls into three categories: \textit{Definition and Concept, Technical Methods and Applications, and Ethical and Social Implications}. (1) \textit{Definition and Concept:} \citet{wang2018conceptions} define the concept of AGI from a point of view of comparison with humans and propose different levels of it. \citet{voss2023concepts} provide direction for the path through the AGI by setting the human-like requirements associated with the AGI. (2) \textit{Technical Methods and Applications:} \citet{yan2022agi,wang2019impact} propose that AGI can be achieved by combining logic with deep learning. \citet{das2023privacy} argues that many risks exist in the development of AGI technology, such as safety and privacy issues.   (3) \textit{Ethical and Social Implications:} \citet{rayhan2023ethical} thinks that humans should consider the ethical implications of creating AGI, which contains impact on human society, privacy, and power dynamics. \citet{bugaj2007five} propose five ethical imperatives and their implications for AGI interactions. These studies have characterized AGI from different aspects. Still, they lack a systematic assessment of the development process of AGI from various aspects and a clear definition of AGI goals, making it difficult to answer the distance between future AGI and current AI and how we can arrive at future AGI.


    In this paper, we conduct a comprehensive survey to answer how far we are from AGI and how we can get to it by clearly establishing the expectation of future AGI and elaborating on the gap between the development of current AI and the expectation. Specifically, we first define the capability system required for future AGI from the three aspects of AGI's internal, interface~(external), and systems. On this basis, we propose that future AGI not only needs to have very powerful capabilities but also needs to meet certain constraints. To design useful and reliable AGI, the technology of AGI alignment is required to align the capabilities and constraints simultaneously. On this basis, we propose the evaluation of AGI to measure the ability of AGI and the satisfaction of constraints. Further, the AGI evaluation can help the researchers locate the current state of AGI  and how far we are from future AGI. Finally, we present case studies from different fields to concretely describe the current development of AI and the expectations and distances of future AGI.
    """

    bibtex_file_path = './main.bib'
    save_file = './cited.txt'
    cited_entries = process_citations(latex_content, bibtex_file_path)
    for entry in cited_entries:
        print(entry)

    with open(save_file, 'w', encoding='utf-8') as file:
        file.write('\n\n'.join(cited_entries))

    if len(cited_entries) == 0:
        print("No BibTeX entries found for the given LaTeX content.")