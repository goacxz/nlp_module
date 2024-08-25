{"nbformat":4,"nbformat_minor":0,"metadata":{"colab":{"provenance":[],"authorship_tag":"ABX9TyMr4ql/aQ4dezbt8f0ur8SZ"},"kernelspec":{"name":"python3","display_name":"Python 3"},"language_info":{"name":"python"}},"cells":[{"cell_type":"code","execution_count":null,"metadata":{"id":"SXKo-oCYfWGJ"},"outputs":[],"source":["import re\n","import os\n","from tqdm import tqdm\n","import numpy as np\n","from typing import List, Tuple, Dict\n","import matplotlib.pyplot as plt\n","\n","\n","def plot_word_frequency(word_count_dict, hist_size=100):\n","    words = list(word_count_dict.keys())[:hist_size]\n","    frequencies = list(word_count_dict.values())[:hist_size]\n","    # 设置图形大小\n","    plt.figure(figsize=(10, 6))\n","    plt.bar(words, frequencies)\n","    plt.title('Word Frequency')\n","    plt.xlabel('Words')\n","    plt.ylabel('Frequency')\n","    plt.xticks(rotation=90)\n","    path_out = 'word_frequency.jpg'\n","    plt.savefig(path_out)\n","    print(f'保存词频统计图:{path_out}')\n","\n","\n","def text_split(content: str) -> List[str]:\n","    \"\"\"\n","    对原始文本进行token化，包含一系列预处理清洗操作\n","    :param content:\n","    :return:\n","    \"\"\"\n","    content = re.sub(r\"([.!?])\", r\" \\1\", content)  # 在 .!? 之前添加一个空格\n","    content = re.sub(r\"[^a-zA-Z.!?]+\", r\" \", content)  # 去除掉不是大小写字母及 .!? 符号的数据\n","    token = [i.strip().lower() for i in content.split()]  # 全部转换为小写，然后去除两边空格，将字符串转换成list,\n","    return token\n","\n","\n","class Vocabulary:\n","    UNK_TAG = \"UNK\"  # 遇到未知字符，用UNK表示\n","    PAD_TAG = \"PAD\"  # 用PAD补全句子长度\n","    UNK = 0  # UNK字符对应的数字\n","    PAD = 1  # PAD字符对应的数字\n","\n","    def __init__(self):\n","        self.inverse_vocab = None\n","        self.vocabulary = {self.UNK_TAG: self.UNK, self.PAD_TAG: self.PAD}\n","        self.count = {}  # 统计词频\n","\n","    def fit(self, sentence_: List[str]):\n","        \"\"\"\n","        统计词频\n","        \"\"\"\n","        for word in sentence_:\n","            self.count[word] = self.count.get(word, 0) + 1\n","\n","    def build_vocab(self, min=0, max=None, max_vocab_size=None) -> Tuple[dict, dict]:\n","        # 词频截断，词频大于或者小于一定数值时，舍弃\n","        if min is not None:\n","            self.count = {word: value for word, value in self.count.items() if value > min}\n","        if max is not None:\n","            self.count = {word: value for word, value in self.count.items() if value < max}\n","        # 选择词表大小，根据词频排序后截断\n","        if max_vocab_size is not None:\n","            raw_len = len(self.count.items())\n","            vocab_size = max_vocab_size if raw_len > max_vocab_size else raw_len\n","            print('原始词表长度:{}，截断后长度:{}'.format(raw_len, vocab_size))\n","            temp = sorted(self.count.items(), key=lambda x: x[-1], reverse=True)[:vocab_size]\n","            self.count = dict(temp)\n","\n","        # 建立词表： token -> index\n","        for word in self.count:\n","            self.vocabulary[word] = len(self.vocabulary)\n","        # 词表翻转：index -> token\n","        self.inverse_vocab = dict(zip(self.vocabulary.values(), self.vocabulary.keys()))\n","\n","        return self.vocabulary, self.inverse_vocab\n","\n","    def __len__(self):\n","        return len(self.vocabulary)\n","\n","\n","if __name__ == '__main__':\n","    max_vocab_size = 20000\n","    path = \"\"  #target path\n","    BASE_DIR = \"\"  #curent path\n","    out_dir = os.path.join(BASE_DIR, 'result')\n","    if not os.path.exists(out_dir):\n","        os.makedirs(out_dir)\n","    vocab_path = os.path.join(out_dir, \"aclImdb_vocab.npy\")\n","    vocab_inv_path = os.path.join(out_dir, \"aclImdb_vocab_inv.npy\")\n","\n","    # 统计词频\n","    vocab_hist = Vocabulary()\n","    temp_data_path = [os.path.join(path, \"pos\"), os.path.join(path, \"neg\")]  # 训练集中包含 正类数据pos 负类数据neg\n","    for data_path in temp_data_path:\n","        file_paths = [os.path.join(data_path, file_name) for file_name in os.listdir(data_path) if file_name.endswith(\"txt\")]\n","        for file_path in tqdm(file_paths):\n","            sentence = text_split(open(file_path, encoding='utf-8').read())\n","            vocab_hist.fit(sentence)\n","\n","    # 建立词表\n","    vocab, inverse_vocab = vocab_hist.build_vocab(max_vocab_size=(max_vocab_size - 2))  # 2 是 unk 和 pad\n","\n","    # 保存词表\n","    np.save(vocab_path, vocab)\n","    np.save(vocab_inv_path, inverse_vocab)\n","\n","    # 词表、词频可视化\n","    print(len(vocab))\n","    word_count = vocab_hist.count\n","    plot_word_frequency(word_count)\n","\n","\n"]}]}