package ASTDecorator;

import ASTGenerator.Data;
import ASTGenerator.MyGson;
import ASTGenerator.Node;
import com.google.gson.JsonIOException;
import com.google.gson.reflect.TypeToken;

import java.util.ArrayList;

public class ASTDecorator implements Decoratable {
	protected Node<Data> astRoot;

	public ASTDecorator(String jsonString) {
		this.astRoot = MyGson.getDataFromJson(jsonString, new TypeToken<Node<Data>>() {
		}.getType());
	}

	public ASTDecorator(Node<Data> root) {
		this.astRoot = root;
	}

	public String decorate() throws JsonIOException {
		while (!isMeaningfulAST(astRoot)) {
			astRoot = dfsWalker(astRoot).get(0);
		}
		// dfsSetParent(astRoot);

		decorateFunctionDeclaration(astRoot);
		decorateFunctionCall(astRoot);
		decorateForNode(astRoot);
		decorateAssignment(astRoot);

		return MyGson.getJsonString(astRoot);
	}

	private ArrayList<Node<Data>> dfsWalker(Node<Data> currentNode) {
		if (currentNode.getData().getContent().isEmpty()) {
			return currentNode.getChildren();
		}
		ArrayList<Node<Data>> tmpChildren = new ArrayList<>();
		for (Node<Data> childNode : currentNode.getChildren()) {
			tmpChildren.addAll(dfsWalker(childNode));
		}
		currentNode.cleanChildren();
		currentNode.addChildren(tmpChildren);
		ArrayList<Node<Data>> arrayList = new ArrayList<>();
		arrayList.add(currentNode);
		return arrayList;
	}

	private boolean isMeaningfulAST(Node<Data> currentNode) {
		if (currentNode.getData().getContent().isEmpty())
			return false;

		for (Node<Data> childNode : currentNode.getChildren()) {
			if (!isMeaningfulAST(childNode))
				return false;
		}
		return true;
	}

	protected Node<Data> createNewNode(String lineNum, String type, String content) {
		Data data = new Data();
		data.setLineNum(lineNum);
		data.setType(type);
		data.setContent(content);
		Node<Data> node = new Node<>(data);
		return node;
	}

	protected Node<Data> searchChild(Node<Data> currentNode, String targetType) {
		for (Node<Data> node : currentNode.getChildren()) {
			if (node.getData().getType().equals(targetType)) {
				return node;
			}
		}
		return null;
	}

	protected boolean containFunctionCall(Node<Data> node) {
		ArrayList<Node<Data>> queue = new ArrayList<>();
		queue.add(node);
		while (!queue.isEmpty()) {
			Node<Data> currentNode = queue.get(0);
			if (currentNode.getData().getType().equals("func_call")) {
				return true;
			}
			queue.remove(0);
			queue.addAll(currentNode.getChildren());
		}
		return false;
	}

	@Override
	public void decorateForNode(Node<Data> currentNode) {

	}

	@Override
	public void decorateFunctionDeclaration(Node<Data> currentNode) {

	}

	@Override
	public void decorateFunctionCall(Node<Data> currentNode) {

	}

	@Override
	public void decorateAssignment(Node<Data> currentNode) {

	}

}
