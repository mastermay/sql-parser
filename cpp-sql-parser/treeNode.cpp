#include "treeNode.h"
#include <iostream>
using std::cout;
using std::endl;
string TreeNode::getData() {
    return data;
}

vector<TreeNode *> TreeNode::getChildren() {
    return children;
}

void TreeNode::add(TreeNode *node) {
    children.push_back(node);
}

TreeNode* TreeNode::go(const string &data) {
    for(auto child : children) {
        if(child->getData() == data) {
            return child;
        }
    }
    return nullptr;
}

void TreeNode::print_node(int num) {
    for(int i=0; i<num; i++) {
        cout<<" ";
    }
    cout<<"+"<<data<<endl;
    for(auto child : children) {
        child->print_node(num+1);
    }
}
