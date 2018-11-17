package ASTDecorator;

import ASTGenerator.Data;
import ASTGenerator.Node;

import java.util.ArrayList;

public class Java8ASTDecorator extends ASTDecorator {
	public Java8ASTDecorator(String jsonString) {
		super(jsonString);
	}

	@Override
	public void decorateForNode(Node<Data> astRoot) {
		ArrayList<Node<Data>> queue = new ArrayList<>();
		queue.add(astRoot);
		while (!queue.isEmpty()) {
			Node<Data> currentNode = queue.get(0);
			if (currentNode.getData().getType().equals("basicForStatement")) {

				String initValue = "", terminationValue = "", increment = "";
				if (currentNode.getChild(0).getData().getType().equals("assignment")) {
					initValue = currentNode.getChild(0).getChild(2).getData().getContent();
				} else if (currentNode.getChild(0).getData().getType().equals("localVariableDeclaration")) {
					initValue = currentNode.getChild(0).getChild(1).getChild(1).getData().getContent();
				}
				terminationValue = currentNode.getChild(1).getChild(1).getData().getContent();
				if (currentNode.getChild(2).getData().getType().equals("postIncrementExpression") || currentNode.getChild(2).equals("preIncrementExpression")) {
					increment = "1";
				} else if (currentNode.getChild(2).getData().getType().equals("postDecrementExpression") || currentNode.getChild(2).equals("preDecrementExpression")) {
					increment = "-1";
				}
				Node<Data> initNode = createNewNode(currentNode.getData().getLineNum(), "startIndex", initValue);
				Node<Data> terminationNode = createNewNode(currentNode.getData().getLineNum(), "endIndex", terminationValue);
				Node<Data> incrementNode = createNewNode(currentNode.getData().getLineNum(), "increment", increment);
				Node<Data> child = currentNode.getChild(3);
				child.getData().setType("body");

				currentNode.cleanChildren();
				currentNode.addChild(initNode);
				currentNode.addChild(terminationNode);
				currentNode.addChild(incrementNode);
				currentNode.addChild(child);
				currentNode.getData().setType("basicForLoop");
			}
			queue.remove(0);
			queue.addAll(currentNode.getChildren());
		}
	}

	@Override
	public void decorateFunctionDeclaration(Node<Data> astRoot) {
		Node<Data> functionNameNode = null, functionBody = null;

		ArrayList<Node<Data>> queue = new ArrayList<>();
		queue.add(astRoot);
		while (!queue.isEmpty()) {
			Node<Data> currentNode = queue.get(0);
			if (currentNode.getData().getType().equals("methodDeclaration")) {
				for (Node<Data> node : currentNode.getChildren()) {
					if (node.getData().getType().equals("methodHeader")) {
						for (Node<Data> grandson : node.getChildren()) {
							if (grandson.getData().getType().equals("methodDeclarator")) {
								String functionName = grandson.getData().getContent();
								// System.out.println(functionName);
								functionNameNode = createNewNode(currentNode.getData().getLineNum(), "func_name", functionName);
							}
						}
					} else if (node.getData().getType().equals("block")) {
						functionBody = node;
						functionBody.getData().setType("body");
					}
				}

				currentNode.cleanChildren();
				currentNode.addChild(functionNameNode);
				currentNode.addChild(functionBody);
				currentNode.getData().setType("func_dcl");
			}
			queue.remove(0);
			queue.addAll(currentNode.getChildren());
		}
	}

	@Override
	public void decorateFunctionCall(Node<Data> astRoot) {
		ArrayList<Node<Data>> queue = new ArrayList<>();
		queue.add(astRoot);
		while (!queue.isEmpty()) {
			Node<Data> currentNode = queue.get(0);
			if (currentNode.getData().getType().contains("methodInvocation")) {
				Node<Data> targetFunction = currentNode.getChild(0);
				targetFunction.getData().setType("func_name");

				currentNode.cleanChildren();
				currentNode.addChild(targetFunction);
				currentNode.getData().setType("func_call");
			}
			queue.remove(0);
			queue.addAll(currentNode.getChildren());
		}
	}

	@Override
	public void decorateAssignment(Node<Data> astRoot) {
		ArrayList<Node<Data>> queue = new ArrayList<>();
		queue.add(astRoot);
		while (!queue.isEmpty()) {
			Node<Data> currentNode = queue.get(0);
			if (currentNode.getData().getType().equals("assignment")) {
				if (!containFunctionCall(currentNode)) {
					currentNode.getData().setType("common_stmt");
				}
			}

			queue.remove(0);
			queue.addAll(currentNode.getChildren());
		}
	}

}
