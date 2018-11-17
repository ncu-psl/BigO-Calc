package ASTDecorator;

import ASTGenerator.Data;
import ASTGenerator.Node;

import java.util.ArrayList;

public class CASTDecorator extends ASTDecorator {
	public CASTDecorator(String jsonString) {
		super(jsonString);
	}

	@Override
	public void decorateForNode(Node<Data> astRoot) {
		ArrayList<Node<Data>> queue = new ArrayList<>();
		queue.add(astRoot);
		while (!queue.isEmpty()) {
			Node<Data> currentNode = queue.get(0);
			if (currentNode.getData().getType().equals("iterationStatement")) {

				Node<Data> forNode = searchChild(currentNode, "forCondition");
				Node<Data> assignmentExpressionNode = searchChild(forNode, "assignmentExpression");

				Node<Data> initNode = assignmentExpressionNode.getChild(2);
				Node<Data> termNode = searchChild(forNode, "relationalExpression").getChild(1);
				Node<Data> incrNode = searchChild(forNode, "postfixExpression");
				if (incrNode == null) {
					incrNode = searchChild(forNode, "prefixExpression");
				}
				String incrementValue = "???";
				if (incrNode.getData().getContent().contains("++")) {
					incrementValue = "1";
				} else if (incrNode.getData().getContent().contains("--")) {
					incrementValue = "-1";
				}

				initNode = createNewNode(initNode.getData().getLineNum(), "startIndex", initNode.getData().getContent());
				termNode = createNewNode(termNode.getData().getLineNum(), "endIndex", termNode.getData().getContent());
				incrNode = createNewNode(incrNode.getData().getLineNum(), "increment", incrementValue);
				Node<Data> bodyNode = searchChild(currentNode, "compoundStatement");
				bodyNode.getData().setType("body");

				currentNode.cleanChildren();
				currentNode.addChild(initNode);
				currentNode.addChild(termNode);
				currentNode.addChild(incrNode);
				currentNode.addChild(bodyNode);
				currentNode.getData().setType("basicForLoop");
			}
			queue.remove(0);
			queue.addAll(currentNode.getChildren());
		}

	}

	@Override
	public void decorateFunctionDeclaration(Node<Data> astRoot) {
		ArrayList<Node<Data>> queue = new ArrayList<>();
		queue.add(astRoot);
		while (!queue.isEmpty()) {
			Node<Data> currentNode = queue.get(0);
			if (currentNode.getData().getType().equals("functionDefinition")) {
				Node<Data> functionNameNode = searchChild(searchChild(currentNode, "directDeclarator"), "directDeclarator");
				Node<Data> functionBody = searchChild(searchChild(currentNode, "compoundStatement"), "blockItemList");
				functionNameNode.getData().setType("func_name");
				functionBody.getData().setType("body");

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
			if (currentNode.getData().getType().equals("postfixExpression")) {
				Node<Data> targetFunction;
				Node<Data> primaryExpressionNode = currentNode.getChild(0);
				if (primaryExpressionNode != null) {
					if (isFunction(primaryExpressionNode)) {
						targetFunction = primaryExpressionNode;
						targetFunction.getData().setType("func_name");
						currentNode.cleanChildren();
						currentNode.addChild(targetFunction);
						currentNode.getData().setType("func_call");
					}
				} else {
					System.out.println("error in CAST decorate");
				}
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
			if (currentNode.getData().getType().equals("assignmentExpression")) {
				if (!containFunctionCall(currentNode)) {
					currentNode.getData().setType("common_stmt");
				}
			}
			queue.remove(0);
			queue.addAll(currentNode.getChildren());
		}
	}

	protected boolean isFunction(Node<Data> primaryExpression) {
		String primary = primaryExpression.getData().getContent();
		ArrayList<Node<Data>> queue = new ArrayList<>();
		queue.add(astRoot);
		while (!queue.isEmpty()) {
			Node<Data> currentNode = queue.get(0);
			if (currentNode.getData().getType().equals("func_dcl")) {
				if (currentNode.getChild(0).getData().getContent().equals(primary)) {
					return true;
				}
			}
			queue.remove(0);
			queue.addAll(currentNode.getChildren());
		}
		return false;
	}

}
