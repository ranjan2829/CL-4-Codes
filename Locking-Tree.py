class Node:
    def __init__(self, label, parent=None):
        self.label = label
        self.parent = parent
        self.children = []
        self.isLocked = False
        self.userID = 0
        self.ancestorLocked = 0
        self.descendantLocked = 0
    def addChildren(self, labels):
        for label in labels:
            child = Node(label, self)
            self.children.append(child)
def buildTree(root, m, labels):
    from collections import deque
    q = deque()
    q.append(root)
    i = 1 
    while q and i < len(labels):
        node = q.popleft()
        children = labels[i:i + m]
        node.addChildren(children)
        for child in node.children:
            q.append(child)
        i += m
    return root
class LockingTree:
    def __init__(self, root):
        self.root = root
        self.labelToNode = {}
        self.fillLabelToNode(root)
        self.output = []
    def fillLabelToNode(self, node):
        if not node:
            return
        self.labelToNode[node.label] = node
        for child in node.children:
            self.fillLabelToNode(child)
    def updateDescendants(self, node, val):
        for child in node.children:
            child.ancestorLocked += val
            self.updateDescendants(child, val)
    def lock(self, label, uid):
        node = self.labelToNode[label]
        if node.isLocked or node.ancestorLocked > 0 or node.descendantLocked > 0:
            return False
        curr = node.parent
        while curr:
            curr.descendantLocked += 1
            curr = curr.parent
        self.updateDescendants(node, 1)
        node.isLocked = True
        node.userID = uid
        return True
    def unlock(self, label, uid):
        node = self.labelToNode[label]
        if not node.isLocked or node.userID != uid:
            return False
        curr = node.parent
        while curr:
            curr.descendantLocked -= 1
            curr = curr.parent
        self.updateDescendants(node, -1)
        node.isLocked = False
        return True
    def checkAndCollectLockedDescendants(self, node, uid, lockedNodes):
        if node.isLocked:
            if node.userID != uid:
                return False
            lockedNodes.append(node)
        if node.descendantLocked == 0:
            return True
        for child in node.children:
            if not self.checkAndCollectLockedDescendants(child, uid, lockedNodes):
                return False
        return True
    def upgrade(self, label, uid):
        node = self.labelToNode[label]
        if node.isLocked or node.ancestorLocked > 0 or node.descendantLocked == 0:
            return False
        lockedNodes = []
        if not self.checkAndCollectLockedDescendants(node, uid, lockedNodes):
            return False
        for desc in lockedNodes:
            self.unlock(desc.label, uid)
        return self.lock(label, uid)
    def processQueries(self, queries):
        for q in queries:
            opcode, label, uid = q
            if opcode == 1:
                self.output.append(str(self.lock(label, uid)).lower())
            elif opcode == 2:
                self.output.append(str(self.unlock(label, uid)).lower())
            elif opcode == 3:
                self.output.append(str(self.upgrade(label, uid)).lower())
    def printOutput(self):
        for line in self.output:
            print(line)

def run_test_case():
    # Test case parameters
    n = 7  # number of nodes
    m = 2  # number of children per node
    q = 5  # number of queries
    
    # Node labels
    labels = ["world", "asia", "africa", "china", "india", "southafrica", "egypt"]
    
    # Queries in format (opcode, label, uid)
    test_queries = [
        (1, "china", 9),    # Lock china with user 9
        (1, "india", 9),    # Lock india with user 9
        (3, "asia", 9),     # Upgrade asia with user 9
        (2, "india", 9),    # Try to unlock india (should fail as it's now unlocked by upgrade)
        (2, "asia", 9)      # Unlock asia with user 9
    ]
    
    # Build tree and process queries
    root = Node(labels[0])
    tree = buildTree(root, m, labels)
    locker = LockingTree(root)
    locker.processQueries(test_queries)
    
    print("Test Case Results:")
    locker.printOutput()

# Run the test
if __name__ == "__main__":
    run_test_case()