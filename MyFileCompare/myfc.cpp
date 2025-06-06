#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
using namespace std;

int main(int argc, char *argv[]) {
    if (argc != 3) {
        cerr << "Usage: " << argv[0] << " <file1> <file2>" << endl;
        return 1;
    }

    ifstream f1(argv[1]), f2(argv[2]);
    if (!f1.is_open() || !f2.is_open()) {
        cerr << "Error opening files" << endl;
        return 1;
    }

    int row = 1;
    while (true) {
        string s1, s2;
        bool b1 = false, b2 = false;

        if (f1) {
            if (getline(f1, s1)) {
                b1 = true;
                size_t endpos = s1.find_last_not_of(' ');
                if (endpos != string::npos) s1 = s1.substr(0, endpos + 1);
                else s1 = "";
            }
        }

        if (f2) {
            if (getline(f2, s2)) {
                b2 = true;
                size_t endpos = s2.find_last_not_of(' ');
                if (endpos != string::npos) s2 = s2.substr(0, endpos + 1);
                else s2 = "";
            }
        }

        if (!b1 && !b2) {
            cout << "AC" << endl;
            return 0;
        }

        if (b1 && !b2) {
            if (s1.empty()) {
                row++;
                continue;
            } else {
                cout << row << " " << 1 << endl;
                return -1;
            }
        }

        if (!b1 && b2) {
            if (s2.empty()) {
                row++;
                continue;
            } else {
                cout << row << " " << 1 << endl;
                return -1;
            }
        }

        if (s1 != s2) {
            int len = min(s1.size(), s2.size());
            int col = 0;
            for (int i = 0; i < len; i++) {
                if (s1[i] != s2[i]) {
                    col = i + 1;
                    break;
                }
            }
            if (col == 0) col = len + 1;
            cout << row << " " << col << endl;
            return -1;
        }

        row++;
    }
}