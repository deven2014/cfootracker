/*
 */
#include <iostream>

using namespace std;

void test1_a(){
    cout << "test1_a()" << endl;
}

void test1_b(){
    cout << "test1_b()" << endl;
    test1_a();
}
