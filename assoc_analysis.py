import numpy as np
import pickle
import argparse
import re
import sys

def read_dataBase(path,min_support,file_type):
    
    if(file_type == 2):
        with open( path, 'rt') as f:
            database = f.read()
        data = re.split(r'[\n]',database)
        tdb = []
        for transactions in data:
            transaction = re.split(' ',transactions)
            tdb.append(transaction)
    else:    
        with open( path, 'rt') as f:
            database = f.read()
        data = re.split(r'[\n]',database)
        
        tdb = {}
        for line in data:
            item = line.split()
            if len(item) == 0:
                continue
            del item[0]
            try:
                tdb[int(item[0])].append(item[1])
            except:
                tdb[int(item[0])] = []
                tdb[int(item[0])].append(item[1])
        tdb = list(tdb.values())
    
    headerTable = gen_headerTable(tdb,min_support)
    
    return tdb,headerTable

def gen_headerTable(tdb,min_support):
    headerTable = {}
    for transaction in tdb:
        for item in transaction:
            try:
               headerTable[item]+= 1
            except:
                headerTable[item] = 1

    for item in list(headerTable):
        if(headerTable[item] < min_support):
            del headerTable[item]
            for i in range( len(tdb) ):
                if item in tdb[i]:
                    tdb[i].remove(item)
    
    return headerTable

def find_assoc(feq_patts_order_list,min_conf):
    
    print("frequent itemset:")
    all_set_count = 0
    for i,items in feq_patts_order_list.items():
        n_set_count = len(items) 
        print("{}_itemset_count:".format(i),n_set_count)
        all_set_count += n_set_count
        #print(items,'\n')
    print("all_itemset_count:",all_set_count,'\n')

    max_itemset_num = 0 
    for item_num in feq_patts_order_list.keys():
        if item_num > max_itemset_num:
            max_itemset_num = item_num
    #print("max_itemset_num:",max_itemset_num)
    
    association_list = {}
    for big in range(max_itemset_num,0,-1):
        for small in range(big-1,0,-1):
                for b_itemset,b_cnt in feq_patts_order_list[big].items():
                    for s_itemset,s_cnt in feq_patts_order_list[small].items():
                        if( set(s_itemset).issubset(b_itemset) ): #test superset
                            # if(s_itemset == b_itemset or b_itemset==() or s_itemset == ()):
                            #     continue
                            if( (b_cnt/s_cnt)>= min_conf ):
                                append_item = tuple(set(b_itemset)-set(s_itemset))
                                
                                if(append_item == () or len(append_item)==0 ):
                                    continue
                                    #print( "\n\n\n",b_itemset,s_itemset,"\n\n\n")
                                    #print(append_item)
                                #print(b_itemset, s_itemset)
                                #print("b_cnt:",b_cnt,"s_cnt:", s_cnt, "b_cnt/s_cnt:", b_cnt/s_cnt,">", min_conf ,"append_item:", append_item)
                                try:
                                    if(append_item not in association_list[s_itemset]):
                                        association_list[s_itemset].append(append_item) 
                                except:
                                    association_list[s_itemset] = [append_item]

    association_cnout = 0
    print("association_list:")
    for itemset,imply_set_list in association_list.items():
        print(itemset,"->",imply_set_list)
        association_cnout += len(imply_set_list)
    #print("association_cnout:",association_cnout)
    print("found {} rules".format(association_cnout))
    
class treeNode:
    def __init__(self, nameValue, num_ccur, parentNode):
        self.name = nameValue
        self.count = num_ccur
        self.nodeLink = None
        self.parent = parentNode 
        self.children = {}

class FPTree:
    def __init__(self,hTable,min_sup):
        self.root = treeNode('Null_Set', 1, None)
        self.headerTable = hTable
        self.min_support = min_sup
    
    def add_tran(self,transaction):
        parent_node = self.root
        for item in transaction:
            if( item not in parent_node.children.keys() ):
                new_node = treeNode(item,1,parent_node)
                parent_node.children[item] = new_node
                self.add_headerTable(item,new_node)
            else:
                parent_node.children[item].count += 1                
                
            parent_node = parent_node.children[item]
            
    def add_headerTable(self, item, new_node):
        if(not self.headerTable[item][1]): #headerTable empty
            self.headerTable[item][1] = new_node
        else:
            nodeToTest = self.headerTable[item][1]
            while(nodeToTest.nodeLink):
                nodeToTest = nodeToTest.nodeLink
            nodeToTest.nodeLink = new_node 
                
    def print_inorder(self,start_node):
        print(start_node.name,start_node.count)
        if(len(start_node.children) != 0):
            for child in start_node.children.values():
                self.print_inorder(child)
        else:
            print("leaf return")
        print("return",start_node.name)
    
    def mining(self):
        feq_patt_all = {}
        for item in self.headerTable.values():
            feq_patt_list = {}
            cpbTroot = self.find_Conditional_Pattern_Base(item[1])
            self.find_feq_patt(cpbTroot, feq_patt_list, [], cpbTroot.count, False)
            del feq_patt_list[tuple()]
            
            for itemset in list(feq_patt_list):
                if feq_patt_list[itemset] < self.min_support:
                    del feq_patt_list[itemset]
            
            for patt,count in list(feq_patt_list.items()):
                
                feq_patt = list(patt)
                feq_patt.append(item[1].name)            
                feq_patt_list[tuple(feq_patt)] = feq_patt_list[patt]
                del feq_patt_list[patt]
                
            feq_patt_all[item[1].name] = feq_patt_list
        return feq_patt_all
        
        
    def find_feq_patt(self, cpBase_root, feq_patt_list, curr_patt, count, duplicated ):
        for ch_node in cpBase_root.children.values():
            self.find_feq_patt(ch_node, feq_patt_list, curr_patt, count, duplicated)
            self.find_feq_patt(ch_node, feq_patt_list, curr_patt + [ch_node.name], ch_node.count, False)
            duplicated = True
        
        if len(cpBase_root.children) or duplicated: return
        try:
            feq_patt_list[tuple(curr_patt)] += count
        except:
            feq_patt_list[tuple(curr_patt)] = count
            
            
    #input一個headertable的起始node return該item(及其link)的cpbT的cpbTroot    
    def find_Conditional_Pattern_Base (self,start_node): 
        cpBase = []
        
        while(start_node): #迭代每個link
            ascendTree = []
            self.find_parents(start_node,ascendTree,start_node.count)
            ascendTree.reverse()
            del ascendTree[0]
            cpBase.append(ascendTree)
            start_node = start_node.nodeLink
        
        cpbTroot = treeNode('Null_Set', 1, None)
        for ascendTree in cpBase:
            self.add_cpbT(cpbTroot,ascendTree)

        return cpbTroot
    
    def find_parents(self,start_node,ascendTree,leaf_count):
        if start_node.parent != None:
            #print(start_node.parent.name)
            new_node = treeNode(start_node.parent.name,leaf_count,start_node.parent.parent)
            ascendTree.append(new_node)
            self.find_parents(start_node.parent, ascendTree,leaf_count)
        
    def add_cpbT(self,cpbTroot,ascendTree):
        parent_node = cpbTroot
        for node in ascendTree:
            if(node.name not in parent_node.children.keys()):
                node.parent = parent_node
                parent_node.children[node.name] = node
            else:
                parent_node.children[node.name].count += node.count                
                
            parent_node = parent_node.children[node.name]
                
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-p',
                        default="fpg",
                        dest='POLICY',
                        help='input policy,default=fpg,fpg=(fpGroeth),apr=apriori')
    parser.add_argument('-msp',
                        default="3",
                        dest='MIN_SUPPORT',
                        help='input min_support,default=3')
    parser.add_argument('-mcf',
                        default="0.5",
                        dest='MIN_CONFIDENCE',
                        help='input min_confidence,default=0.5')
    parser.add_argument('-f',
                        default="data.ntrans_1",
                        dest='DATA_FILE',
                        help='input database,default=data.ntrans_1')
    parser.add_argument('-ftp',
                        default="1",
                        dest='FILE_TYPE',
                        help='input file type,default=1(IBM-Quest-Data-Generator)')
    args = parser.parse_args()

    policy = args.POLICY
    min_support = int(args.MIN_SUPPORT)
    min_conf = float(args.MIN_CONFIDENCE)
    data_file = args.DATA_FILE
    file_type = int(args.FILE_TYPE)
    print("policy:",policy)
    print("min_support:",min_support)
    print("min_conf:",min_conf)
    print("data_file:",data_file,"\n")
    
    
    if(policy == "fpg"):
        tdb,headerTable = read_dataBase(data_file,min_support,file_type)
        sort_db = [sorted(t, key = lambda item:headerTable[item], reverse = True) for t in tdb ]
        
        for item in headerTable:
            headerTable[item] = [headerTable[item], None]
        #print("init_headerTable:",headerTable,'\n')    
        #print("sort_db:",sort_db,'\n')

        fptree = FPTree(headerTable,min_support)
        
        for transaction in sort_db:
            fptree.add_tran(transaction)
        #print("fptree:")
        #fptree.print_inorder(fptree.root)
        
        feq_patts_list = fptree.mining()
        #print("feq_patts_list:",feq_patts_list,'\n')
        #print("feq_patts_list:")
        #for head, feq_patts in feq_patts_list.items():
        #    print(head,feq_patts)
        #print('\n')
        
        #print("headerTable:")    
        #for item,ifo in headerTable.items():
        #    print(item)
        #    start = ifo[1]
        #    while(start):
        #        print(start.name,"parent:",start.parent.name)
        #        start = start.nodeLink
        
        feq_patts_order_list = {}
        #補 one_itemset
        feq_patts_order_list[1]={}
        for item,info in fptree.headerTable.items():
            feq_patts_order_list[1][tuple([item])] = info[0]
        
        for head,feq_patts in feq_patts_list.items():
            #print(feq_patts)
            if len(feq_patts) == 0 : continue
            for patt,cnt in feq_patts.items():
                #print("patt",patt,len(patt),cnt)
                try:
                    feq_patts_order_list[len(patt)][patt] = cnt
                except:
                    feq_patts_order_list[len(patt)] = {}
                    feq_patts_order_list[len(patt)][patt] = cnt
        #print("feq_patts_order_list:",feq_patts_order_list)
        #print("feq_patts_order_list:")
        
    elif(policy == "apr"):
        
        tdb,headerTable = read_dataBase(data_file,min_support,file_type)
        c_table = {}
    
        #C1
        c1 = {}    
        for transaction in tdb:
            for item in transaction:
                try:
                    c1[tuple([item])]+= 1
                except:
                    c1[tuple([item])] = 1

        for itemset in list(c1):
            if(c1[itemset] < min_support):
                del c1[itemset]

        c_table[1] = c1
        #print("only one c_table:",c_table,'\n')

        k = 2
        while(True):
            current_c = {}
            #gen ck
            for i,itemset in enumerate( c_table[k-1].keys() ):
                for j,pick_itemset in enumerate( c_table[k-1].keys() ):
                    #print(i,j,itemset,pick_itemset)
                    if(j<=i):
                        continue
                    else:
                        new_itemset = tuple(sorted( set(itemset) | set(pick_itemset)) )
                        if(len(new_itemset) == k):
                            current_c[new_itemset] = 0
                            #scan DB
                            for item in tdb:
                                if ( not (set(new_itemset) - set(item)) ):  #有此筆data
                                    current_c[new_itemset] += 1
                            #check min suuport        
                            if(current_c[new_itemset] < min_support):
                                #print("del:",itemset)
                                del current_c[new_itemset]    
            
            if(len(current_c) == 0):
                break
            c_table[k] = current_c
            k += 1
        
        feq_patts_order_list = c_table
        #print("c_table:",c_table)
        
    else:
        print("Please use -p to specify your policy,fpg=fpGroeth,apr=apriori")
        sys.exit()

    find_assoc(feq_patts_order_list,min_conf)
