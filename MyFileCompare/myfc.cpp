#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <cctype>

// 去除字符串右侧的空格和制表符
std::string rtrim(const std::string &s) {
    auto end = std::find_if_not(s.rbegin(), s.rend(), [](int ch) {
        return std::isspace(ch);
    });
    return std::string(s.begin(), end.base());
}

// 比较两个文件，忽略行末空格和文件末尾多余的空行
bool compareFiles(const std::string& file1, const std::string& file2) {
    std::ifstream f1(file1), f2(file2);
    if (!f1.is_open() || !f2.is_open()) {
        std::cerr << "无法打开文件" << std::endl;
        return false;
    }

    std::string line1, line2;
    bool hasMore1, hasMore2;

    while (true) {
        // 读取文件1的一行（跳过空行）
        hasMore1 = false;
        while (std::getline(f1, line1)) {
            line1 = rtrim(line1);
            if (!line1.empty()) {
                hasMore1 = true;
                break;
            }
        }

        // 读取文件2的一行（跳过空行）
        hasMore2 = false;
        while (std::getline(f2, line2)) {
            line2 = rtrim(line2);
            if (!line2.empty()) {
                hasMore2 = true;
                break;
            }
        }

        // 检查是否到达文件末尾
        if (!hasMore1 && !hasMore2) {
            return true; // 两个文件都结束，内容相同
        }
        if (!hasMore1 || !hasMore2) {
            return false; // 一个文件结束，另一个还有内容
        }

        // 比较非空行
        if (line1 != line2) {
            return false;
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "usage: " << argv[0] << " <file1> <file2>" << std::endl;
        return 1;
    }

    if (compareFiles(argv[1], argv[2])) {
        std::cout << "ac" << std::endl;
        return 0;
    } else {
        std::cout << "wa" << std::endl;
        return 1;
    }
}