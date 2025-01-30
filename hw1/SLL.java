class SinglyLinkedList {
    // Node class to represent each element in the list
    private static class Node {
        int data;
        Node next;

        Node(int data) {
            this.data = data;
            this.next = null;
        }
    }

    // Instance variables for the linked list
    private Node head; // Points to the first node
    private Node tail; // Points to the last node
    private int size; // Number of elements in the list

    // Constructor to initialize an empty list
    public SinglyLinkedList() {
        this.head = null;
        this.tail = null;
        this.size = 0;
    }

    // Method to add an element at the end of the list
    public void addLast(final int data) {
        final Node node = new Node(data);
        if (head == null) {
            head = node;
            tail = node;
        } else {
            tail.next = node;
            tail = node;
        }
        size++;
    }

    // Method to add an element at the beginning of the list
    public void addFirst(final int data) {
        final Node node = new Node(data);
        node.next = head;
        head = node;
        if (tail == null)
            tail = node;
        size++;
    }

    // Method to print all keys at even positions
    public void printEvenPositions() {
        int currIndex = 1;
        Node currNode = head;
        while (currNode != null) {
            if (currIndex % 2 == 0)
                System.out.print(currNode.data + " ");

            currNode = currNode.next;
            currIndex++;
        }
        System.out.println();
    }

    // Method to search for a given key and return the index (1-based)
    public int search(final int key) {
        int currIndex = 1;
        Node currNode = head;
        while (currNode != null) {
            if (currNode.data == key)
                return currIndex;
            currNode = currNode.next;
            currIndex++;
        }
        return -1;
    }

    // Method to count occurrences of a given key
    public int countOccurrences(final int key) {
        int occ = 0;
        Node currNode = head;
        while (currNode != null) {
            if (currNode.data == key)
                occ++;
            currNode = currNode.next;
        }
        return occ;
    }

    // Method to add an element at a given position (1-based index)
    public int addAtPosition(final int data, final int position) {
        if (position < 1 || position > this.size + 1)
            return -1;

        final Node node = new Node(data);

        Node prevNode = new Node(-1);
        prevNode.next = this.head;
        Node currNode = this.head;
        int index = 1;
        while (prevNode != null) {
            if (index == position) {
                prevNode.next = node;
                node.next = currNode;

                if (index == 1)
                    this.head = node;
                if (index == this.size + 1)
                    this.tail = node;

                size++;
                return index;
            }

            prevNode = currNode;
            if (currNode != null)
                currNode = currNode.next;
            index++;
        }
        return -1; // unreachable
    }

    // Method to remove the first element
    public boolean removeFirst() {
        if (head == null)
            return false;

        head = head.next;
        if (head == null) {
            tail = null;
        }
        size--;
        return true;
    }

    // Method to remove the last element
    public boolean removeLast() {
        if (head == null)
            return false;

        if (head == tail) {
            head = null;
            tail = null;
        } else {
            Node current = head;
            while (current.next != tail) {
                current = current.next;
            }
            current.next = null;
            tail = current;
        }
        size--;
        return true;
    }

    // Method to remove an element by key
    public int removeKey(final int key) {
        Node prevNode = new Node(-1);
        prevNode.next = this.head;
        Node currNode = this.head;
        while (prevNode != null) {
            if (currNode != null && currNode.data == key) {
                prevNode.next = currNode.next;
                this.size--;
                return 0;
            }

            prevNode = currNode;
            if (currNode != null)
                currNode = currNode.next;
        }
        return -1;
    }

    // Method to remove an element at a given position (1-based index)
    public int removeAtPosition(final int position) {
        if (position < 1 || position > this.size)
            return -1;

        Node prevNode = new Node(-1);
        prevNode.next = this.head;
        Node currNode = this.head;
        int index = 1;
        while (prevNode != null) {
            if (currNode != null && index == position) {
                prevNode.next = currNode.next;

                if (index == 1)
                    this.head = currNode.next;
                if (index == this.size)
                    this.tail = index == 1 ? null : prevNode;

                this.size--;
                return 0;
            }

            prevNode = currNode;
            if (currNode != null)
                currNode = currNode.next;
            index++;
        }
        return -1;
    }

    // Method to print the elements of the list
    public void print() {
        Node current = head;
        while (current != null) {
            System.out.print(current.data + " -> ");
            current = current.next;
        }
        System.out.printf("null [%d]\n", this.size);
    }
}

class Main {
    public static void main(String[] args) {
        SinglyLinkedList list = new SinglyLinkedList();

        // Initial operations
        list.addLast(10);
        list.addLast(20);
        list.addLast(30);
        list.addLast(30);
        list.addLast(20);
        list.addLast(10);
        list.addLast(10);
        list.addLast(20);
        list.addLast(30);
        list.addFirst(40);
        list.addFirst(50);
        list.removeFirst(); // Removes 50
        list.removeFirst(); // Removes 40
        list.removeLast(); // Removes 30
        list.removeLast(); // Removes 20
        list.print(); // 10 -> 20 -> 30 -> 30 -> 20 -> 10 -> 10 -> null

        list.printEvenPositions(); // 20 30 10
        list.addFirst(20); // Adds 20 at the start
        list.printEvenPositions(); // 10 30 20 10

        list.addAtPosition(60, 1); // Adds 60 at position 1
        list.addAtPosition(20, 6); // Adds 20 at position 6
        list.addAtPosition(30, 7); // Adds 30 at position 7
        list.addAtPosition(50, 15); // Position 15 is invalid and hence 50 is not added
        list.print();

        int index = list.search(70);
        System.out.println("First index of 70: " + index); // -1 (70 is not in the list)

        index = list.search(10);
        System.out.println("First index of 10: " + index); // 3

        index = list.search(60);
        System.out.println("First index of 60: " + index); // 1

        int count = list.countOccurrences(70);
        System.out.println("Occurrences of 70: " + count); // 0 (70 is not in the list)

        count = list.countOccurrences(30);
        System.out.println("Occurrences of 30: " + count); // 4

        count = list.countOccurrences(60);
        System.out.println("Occurrences of 60: " + count); // 1
        list.print();

        list.removeKey(30); // Removes the first occurrence of 30
        list.removeKey(30); // Removes the next occurrence of 30
        list.removeKey(30); // Removes the last occurrence of 30
        list.removeKey(30); // 30 does not appear and hence it cannot be removed
        list.print(); // 60 -> 20 -> 10 -> 20 -> 20 -> 20 -> 10 -> 10 -> null

        list.removeAtPosition(1); // Removes the first element (60)
        list.print();
        list.removeAtPosition(7); // Removes the last element (10)
        list.print();
        list.removeAtPosition(7); // Position invalid and hence does nothing
        list.print(); // 20 -> 10 -> 20 -> 20 -> 20 -> 10 -> null
    }
}

/*
 * Expected Output:
 * 
 * 10 -> 20 -> 30 -> 30 -> 20 -> 10 -> 10 -> null
 * Keys at even positions: 20 30 10
 * Keys at even positions: 10 30 20 10
 * 60 -> 20 -> 10 -> 20 -> 30 -> 20 -> 30 -> 30 -> 20 -> 10 -> 10 -> null
 * First index of 70: -1
 * First index of 10: 3
 * First index of 60: 1
 * Occurrences of 70: 0
 * Occurrences of 30: 3
 * Occurrences of 60: 1
 * 60 -> 20 -> 10 -> 20 -> 20 -> 20 -> 10 -> 10 -> null
 * 20 -> 10 -> 20 -> 20 -> 20 -> 10 -> null
 */
