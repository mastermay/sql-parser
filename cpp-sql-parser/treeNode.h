#ifndef _TREENODE_H_
#define _TREENODE_H_

#include <iostream>
#include <vector>
#include <string>
using std::string;
using std::vector;

class TreeNode {
public:
    TreeNode(const string &s) : data(s) {}
    string getData();
    vector<TreeNode *> getChildren();
    void add(TreeNode *node);
    TreeNode* go(const string &data);
    void print_node(int num);

private:
    string data;
    vector<TreeNode *> children;
};

#endif // _TREENODE_H_
