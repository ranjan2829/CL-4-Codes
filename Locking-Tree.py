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
    i = 1  # Start from the second label

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

        # Update ancestor's descendantLocked count
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


# Driver
n = int(input())
m = int(input())
q = int(input())
labels = [input().strip() for _ in range(n)]

root = Node(labels[0])
tree = buildTree(root, m, labels)

locker = LockingTree(root)

queries = []
for _ in range(q):
    opcode, label, uid = input().split()
    queries.append((int(opcode), label, int(uid)))

locker.processQueries(queries)
locker.printOutput()
