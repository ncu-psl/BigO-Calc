package ASTGenerator;

import java.io.Serializable;
import java.util.ArrayList;

public class Node<T> implements Serializable, Cloneable {
	private static final long serialVersionUID = 1L;

	private T data;
	private transient Node<T> parent;
	private ArrayList<Node<T>> children = new ArrayList<>();

	public Node() {
	}

	public Node(T data) {
		this.data = data;
	}

	public T getData() {
		return data;
	}

	public void setData(T data) {
		this.data = data;
	}

	public ArrayList<Node<T>> getChildren() {
		return children;
	}

	public Node<T> getChild(int index) {
		if (children.isEmpty()) {
			return null;
		}

		return children.get(index);
	}

	public int getChildCount() {
		if (children.isEmpty()) {
			return 0;
		}
		return children.size();
	}

	public void addChild(Node<T> node) {
		children.add(node);
		node.setParent(this);
	}

	public void addChildren(ArrayList<Node<T>> children) {
		for (Node<T> child : children)
			this.children.add(child);
	}

	public void cleanChildren() {
		children.clear();
	}

	public void resetChildren(ArrayList<Node<T>> children) {
		cleanChildren();
		this.children = children;
	}

	public Node<T> getParent() {
		return parent;
	}

	public void setParent(Node<T> parent) {
		this.parent = parent;
	}

	// @Override
	// public Object clone() throws CloneNotSupportedException {
	// Node<T> node = (Node<T>) super.clone();
	// if (parent != null)
	// node.parent = (Node<T>) this.parent.clone();
	// else
	// node.parent = null;
	// node.children = (ArrayList<Node<T>>) this.children.clone();
	// // node.data = (T) this.data.clone();
	// return node;
	// }
}
