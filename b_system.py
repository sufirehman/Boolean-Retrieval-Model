import nltk
import collections
import math
import sys
from unittest import result

#Using Binary tree
class Nodes(object):
    """Tree node: left and right children + data which is object"""

    def __init__(s, data):
        #constructor @param data node data object
        s.left = None
        s.right = None
        s.data = data

    def insert(s, data):
        #Insert new node with data at present data node data object to insert
        if(s.data):
            if (data > s.data):
                if(s.right is None):
                    s.right = Nodes(data)
                else:
                    s.right.insert(data)
            elif(data < s.data):
                if(s.left is None):
                    s.left = Nodes(data)
                else:
                    s.left.insert(data)
        else:
            s.data = data

    def btree_data(s):
        """To get tree nodes data"""
        # Using a stack to traverse tree in a non-recursive manner
        node = s
        st = []          #stack for nodes
        while(st or node):
            if (node):
                st.append(node)
                node = node.left
            else:
                # we are returning so we pop the node and yield it
                node = st.pop()
                yield node.data         #returns node's data
                node = node.right

class BRsystem():

    def __init__(s, docs=None, stop_words=[]):      
        s._docs = docs
        s.stemmer = nltk.stem.porter.PorterStemmer()
        s.inv_index = s.preprocess(stop_words)
        s.print_inv_index()

    def posting_list(s, word):   
        return [doc_id for doc_id in s.inv_index[word].btree_data() if doc_id != None] # to return document id's for each term

    def print_inv_index(s):         
        #Printing Inverted Index after stemming
        print('Inverted Index:\n')
        for w, t in s.inv_index.items():
            print('{}: {}'.format(w, [docid for docid in t.btree_data() if docid != None]))
        print()

    def preprocess(s, stopwords):       #Preprocessing, removing stop words, and tokenizing 
        ind = {}
        for i, doc in enumerate(s._docs):        #parsing through all files
            for word in doc.split():             #tokenization
                if(word in stopwords):
                    continue
                token = s.stemmer.stem(word.lower())      #stemming performed and stored as tokens
                if (ind.get(token, -448) == -448):           
                    ind[token] = Nodes(i + 1)            #object callable
                elif(isinstance(ind[token], Nodes)):
                    ind[token].insert(i + 1)
        return ind

    @staticmethod
    def parse(tokens):
        """Using Shunting yard algorithm to parse query"""
        precedence = {}
        precedence['OR'] = 1             #precedence set for each operator
        precedence['AND'] = 2
        precedence['NOT'] = 3
        precedence['or'] = 1             #precedence set for each operator
        precedence['and'] = 2
        precedence['not'] = 3

        result = []
        op_stack = []

        for t in tokens:
            # if operator, pop operators from operator stack to queue if they are of higher precedence
            if (t in precedence):
                # if operator stack is not empty
                if (op_stack):
                    c_op = op_stack[-1]
                    while (precedence[c_op] > precedence[t] and op_stack): #if op stack !empty and precedence of current operator is greater then
                        result.append(op_stack.pop())          
                        if (op_stack):
                            c_op = op_stack[-1]
                op_stack.append(t)                  # adds token to stack
            else:
                result.append(t.lower())

        # pop operators into queue(result) if still present in stack
        while (op_stack):
            result.append(op_stack.pop())

        return result

    def or_operation(left_op, right_op):
        l_index = 0     #current index in left operand
        r_index = 0     #current index in right operand
        result = []     #for union of left and right operands

        # while list has not yet been covered
        while (r_index < len(right_op) or l_index < len(left_op)):
            # if both list is not yet exhausted
            if (l_index < len(left_op) and r_index < len(right_op)):
                left_item = left_op[l_index]  # current item in left_operand
                right_item = right_op[r_index] # current item in right_operand
                
                # right item greater than left item, add left item and expand left index
                if (left_item < right_item):
                    result.append(left_item)
                    l_index += 1

                # if items are equal, add one to result and move both pointers
                elif (left_item == right_item):
                    result.append(left_item)
                    l_index += 1
                    r_index += 1

                # right item greater than left item, add left item and expand left index
                elif (left_item < right_item):
                    result.append(left_item)
                    l_index += 1

                # left item greater than right_item, add right item and expand right index
                else:
                    result.append(right_item)
                    r_index += 1

            # if left_operand list is exhausted, append right item and expand right index
            elif (l_index >= len(left_op)):
                right_item = right_op[r_index]
                result.append(right_item)
                r_index += 1

            #if right_operand list is exhausted, append left item and epand l_index 
            else:
                l_item = left_op[l_index]
                result.append(left_item)
                l_index += 1

        return result

    @staticmethod
    def and_operation(l_operand, r_operand):

        #Using skip pointers for this as intersection between terms is hectic comparison
        right_skip = int(math.sqrt(len(r_operand))) #Taking square root of right node as skip pointer distance 
        left_skip = int(math.sqrt(len(l_operand)))  # Taking square root of left node as skip pointer distance

        r_index = 0                                 # current index in right operand
        l_index = 0                                 # current index in left operand
        result = []                                 # results list to be returned

        while (r_index < len(r_operand) and l_index < len(l_operand)):
            l_item = l_operand[l_index]  # current item in left_operand
            r_item = r_operand[r_index] # current item in right_operand
            
            # if left item is greater than right item
            if (l_item > r_item):
                # if r_index can be skipped (if new r_index is still within range and resulting item is <= left item)
                if (len(r_operand) > r_index + right_skip  and r_operand[r_index + right_skip] <= l_item):
                    r_index += right_skip         #jump
                # else advance right index by 1
                else:
                    r_index += 1

            # match
            elif (l_item == r_item):
                result.append(l_item)   # add to results
                r_index += 1            # advance right index
                l_index += 1            # advance left index

            # if left item is smaller than right item
            else:
                # if l_index can be skipped (if new l_index is still in range and resulting item is <= right item)
                if (len(l_operand) > l_index + left_skip and l_operand[l_index + left_skip] <= r_item):
                    l_index += left_skip
                # else advance l_index by 1
                else:
                    l_index += 1

        return result

    @staticmethod
    def not_operation(right_op, docids):
        # Opposite of an empty list gives list of all indexed docIDs
        if (not right_op):
            return docids
        r_index = 0 # index for right operand
        r_list = []
        for m in docids:
            # if item do not match with right operand, it belongs to compliment 
            if (m != right_op[r_index]):
                r_list.append(m)
            # if item matches and right index still can progress, advance it by 1
            elif (len(right_op) > r_index + 1):
                r_index += 1
        return r_list

    def process(self, query):

        # prepares list of query
        r_stack = []
        query = query.lower().split(' ')   #splitting query and separating words and operators
        v_docids = list(range(1, len(self._docs) + 1))     
        final_queue = collections.deque(self.parse(query))    # get query in postfix notation in a queue

        while(final_queue):
            result = []                         # the evaluated result at each stage
            token = final_queue.popleft()
            # if operand, adds postings list for the term to r_stack
            if ( token != 'OR' and token != 'or' and token!='AND' and token != 'and' and token!='NOT' and token!='not'):
                token = self.stemmer.stem(token)                      # stem the token
                # default empty list if not in dictionary
                if (token in self.inv_index):
                    result = self.posting_list(token)
            
            elif (token == 'OR' or token=='or'):
                r_operand = r_stack.pop()
                l_operand = r_stack.pop()
                result = BRsystem.or_operation(l_operand, r_operand)    # evaluates OR

            elif (token == 'AND' or token=='and'):
                r_operand = r_stack.pop()
                l_operand = r_stack.pop()
                result = BRsystem.and_operation(l_operand, r_operand)   # evaluates AND

            elif (token == 'NOT' or token=='not'):
                right_operand = r_stack.pop()
                result = BRsystem.not_operation(r_operand, v_docids) # evaluates NOT

            r_stack.append(result)                        

        # at this point result stack should only have 1 item
        if len(r_stack) != 1: 
            print("Invalid Query.") # checks error
            return None
        
        return r_stack.pop()