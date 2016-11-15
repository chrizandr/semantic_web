##########################################################################################
## Semantic Web Form                                                                    ##
## Authors : Chris Andrew, Santhoshini Reddy                                            ##
## Email: chris.g14@iiits.in ; santhoshini.g14@iiits.in                                 ##
## Github: https://github.com/chrizandr ; https://github.com/Sanny26                    ##
###################################################################                     ##
## Description: This project was developed as part of the SEFP course at IIIT Sri City  ##
## All code is available for free usage for educational purposes                        ##
## Authors do not authorize commercial use of the source code                           ##
##########################################################################################

################### Imports ##################


################### Source ##################
# ----------------------------------------------------------------------------------------
# create_dict : funciton to create a dictionary of classes
def create_dict(node, node_id, parent_id):
    node_dict = dict()
    node_dict["id"] = node_id
    node_dict["text"] = (str(node).split('#')[-1]).strip('*>')
    node_dict["parentid"] = parent_id
    return node_dict


# ----------------------------------------------------------------------------------------
# getAllChildren : funciton to decide which class is a child
def getAllChildren(node, class_id):
    child_list = list()
    parentid = class_id
    class_id += 1
    for child in node.children():
        class_dict = create_dict(child, class_id, parentid)
        child_list.append(class_dict)
        sub_list = getAllChildren(child, class_id)
        class_id += 1
        for each_dict in sub_list:
            class_id += 1
            child_list.append(each_dict)
    return child_list


# ----------------------------------------------------------------------------------------
# generateTree : funciton to generate a final tree of classes and properties
def generateTree(graph):
    classlist = list()
    class_id = 1
    for each_class in graph.toplayer:
        class_dict = create_dict(each_class, class_id, -1)
        child_list = getAllChildren(each_class, class_id)
        classlist.append(class_dict)
        for each_child in child_list:
            class_id += 1
            classlist.append(each_child)
        class_id += 1
    return classlist
