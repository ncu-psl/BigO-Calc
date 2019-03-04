package Main;

import BigOAST.*;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Optional;

public class TimeComplexityCalculator {
	private List<FunctionDeclarationNode> funcDclNodes;

	public TimeComplexityCalculator() {

	}

	public List<FunctionDeclarationNode> getFuncDclNodes() {
		return funcDclNodes;
	}

	public void setFuncDclNodes(List<FunctionDeclarationNode> funcDclNodes) {
		this.funcDclNodes = funcDclNodes;
	}

	public void calculate(CompilationUnitNode cu) {
		this.setFuncDclNodes(getFunctionDeclarationNodes(cu));

		// recursive function filter
		doSearchRecursiveFunction(funcDclNodes);

		// calculate time complexity
		System.out.println("[Time Complexity]");
		for (FunctionDeclarationNode funcDclNode : funcDclNodes) {
			if (!funcDclNode.isRecursive())
				calculate(funcDclNode, funcDclNode);
			System.out.println(funcDclNode.getName() + "=" + funcDclNode.getTimeComplexity());
		}
	}

	private List<FunctionDeclarationNode> getFunctionDeclarationNodes(CompilationUnitNode cu) {
		List<FunctionDeclarationNode> funcDclNodes = new ArrayList<>();

		// bfs
		List<BasicNode> queue = new LinkedList<>();
		queue.add(cu);
		while (!queue.isEmpty()) {
			BasicNode node = queue.get(0);
			if (node.getClass().equals(FunctionDeclarationNode.class)) {
				funcDclNodes.add((FunctionDeclarationNode) node);
			}
			queue.remove(0);
			queue.addAll(node.getChildren());
		}
		return funcDclNodes;
	}

	private void doSearchRecursiveFunction(List<FunctionDeclarationNode> funcDclNodes) {
		for (FunctionDeclarationNode funcDclNode : funcDclNodes) {
			if (isRecursiveFunction(funcDclNode)) {
				funcDclNode.setRecursive(true);
				funcDclNode.setTimeComplexity("IsRecursiveFunction");
			}
		}
	}

	private boolean isRecursiveFunction(FunctionDeclarationNode funcDclNode) {
		// bfs
		List<BasicNode> queue = new LinkedList<>();
		queue.add(funcDclNode);
		while (!queue.isEmpty()) {
			BasicNode node = queue.get(0);
			if (node.getClass().equals(FunctionCallNode.class)) {
				if (((FunctionCallNode) node).getName().equals(funcDclNode.getName())) {
					return true;
				}
			}
			queue.remove(0);
			queue.addAll(node.getChildren());
		}
		return false;
	}

	private String calculate(BasicNode currentNode, BasicNode parentNode) {
		String myTC = "";
		if (currentNode.getClass().equals(ForNode.class)) {
			ForNode forNode = (ForNode) currentNode;
			String init = forNode.getInit(), term = forNode.getTerminal();
			if (forNode.getUpdate().equals("+1")) {
				myTC = "(" + term + " - " + init + ")";
			}
		} else if (currentNode.getClass().equals(FunctionCallNode.class)) {
			// function call
			FunctionCallNode funcCallNode = ((FunctionCallNode) currentNode);
			Optional<FunctionDeclarationNode> funcDclNode = getFunctionDclNodeByName(funcCallNode.getName());

			// check if function exist
			if (!funcDclNode.isPresent()) {
				System.err.println("funcDclNode not found: " + funcCallNode.getName());
			} else {
				String timeComplexity = funcDclNode.get().getTimeComplexity();
				if (timeComplexity != null && !timeComplexity.isEmpty()) {
					myTC = "(" + funcDclNode.get().getName() + ")";
				} else {
					calculate(funcDclNode.get(), funcDclNode.get());
				}
			}
		} else {
			myTC = "(1)";
		}

		// recursively calculate children's time complexity
		StringBuilder childrenTC = new StringBuilder();
		for (BasicNode node : currentNode.getChildren()) {
			childrenTC.append(calculate(node, currentNode));
			childrenTC.append("+");
		}
		if (childrenTC.length() > 0) {
			childrenTC.delete(childrenTC.length() - 1, childrenTC.length());
			myTC = myTC + "*(" + childrenTC.toString() + ")";
		}

		currentNode.setTimeComplexity(myTC);
		return currentNode.getTimeComplexity();
	}

	private static boolean isInteger(String str) {
		return str.matches("(\\+-)?\\d+");
	}

	private Optional<FunctionDeclarationNode> getFunctionDclNodeByName(String name) {
		for (FunctionDeclarationNode funcDclNode : funcDclNodes) {
			if (funcDclNode.getName().equals(name)) {
				return Optional.of(funcDclNode);
			}
		}
		return Optional.empty();
	}
}
