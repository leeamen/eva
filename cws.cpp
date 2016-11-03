#include <string>
#include "segment_dll.h"

int main(int argc, char * argv[]) {
    if (argc < 2) {
        std::cerr << "cws [model path]" << std::endl;
        return 1;
    }

    void * engine = segmentor_create_segmentor(argv[1]);//分词接口，初始化分词器
    if (!engine) {
        return -1;
    }
    std::vector<std::string> words;
    int len = segmentor_segment(engine,
            "爱上一匹野马，可我的家里没有草原。", words);//分词接口，对句子分词。
    for (int i = 0; i < len; ++ i) {
        std::cout << words[i] << "|";
    }
    std::cout << std::endl;
    segmentor_release_segmentor(engine);//分词接口，释放分词器
    return 0;
}
