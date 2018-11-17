package ASTGenerator;

import com.google.gson.reflect.TypeToken;

import java.util.ArrayList;

public class TimeComplexityCalculator {
	Node<Data> astRoot;

	public Node<Data> getAstRoot() {
		return astRoot;
	}

	public void setAstRoot(Node<Data> astRoot) {
		this.astRoot = astRoot;
	}

	public void setAstRoot(String jsonString) {
		this.astRoot = MyGson.getDataFromJson(jsonString, new TypeToken<Node<Data>>() {
		}.getType());
	}

	private void dfsSetParent(Node<Data> currentNode) {
		for (Node<Data> childNode : currentNode.getChildren()) {
			childNode.setParent(currentNode);
			dfsSetParent(childNode);
		}
	}

	public String calculate() {
		if (astRoot.getChild(0).getParent() == null) {
			dfsSetParent(astRoot);
		}
		calculate(astRoot);
		addFunctionRP();
		return MyGson.getJsonString(astRoot);
	}

	private String calculate(Node<Data> node) {
		if (!node.getData().getTimeComplexity().isEmpty()) {
			return node.getData().getTimeComplexity();
		}
		if (node.getData().getType().equals("basicForLoop")) {
			int staIndex = 0, endIndex = 0, increment = 0;

			String staValue = node.getChild(0).getData().getContent();
			boolean predictable = true;
			if (staValue.matches("-?\\d+")) {
				staIndex = Integer.valueOf(staValue);
			} else {
				predictable = false;
			}
			String endValue = node.getChild(1).getData().getContent();
			if (endValue.matches("-?\\d+")) {
				endIndex = Integer.valueOf(endValue);
			} else {
				predictable = false;
			}
			String incValue = node.getChild(2).getData().getContent();
			if (incValue.matches("\\w\\+=\\d+") || incValue.matches("\\+?1")) {
				increment = Integer.valueOf(incValue);
			} else {
				predictable = false;
			}
			if (predictable) {
				node.getData().setTimeComplexity(Math.abs(endIndex - staIndex) + "*(");
			} else {
				node.getData().setTimeComplexity("((" + endValue + "-" + staValue + ")/" + incValue + ")*(");
			}
		} else if (node.getData().getType().equals("func_call")) {
			if (!checkRecursion(node.getChild(0))) {
				String methodTimeComplexity = getMethodTimeComplexity(node);
				if (methodTimeComplexity == null) {
					System.err.println("[calculator]function not found: " + node.getData().getContent());
					methodTimeComplexity = "1+";
				}
				node.getData().setTimeComplexity(methodTimeComplexity);
			}
		} else if (node.getData().getType().equals("common_stmt")) {
			node.getData().setTimeComplexity("1+");
		}
		for (Node<Data> child : node.getChildren()) {
			String timeComplexity = calculate(child);
			if (!timeComplexity.equals("is a recursive function")) {
				node.getData().setTimeComplexity(node.getData().getTimeComplexity() + timeComplexity);
			} else {
				// System.out.println();
			}
		}
		return node.getData().getTimeComplexity();
	}

	private String getMethodTimeComplexity(Node<Data> node) {
		String methodName = node.getChild(0).getData().getContent();
		ArrayList<Node<Data>> queue = new ArrayList<>();
		queue.add(astRoot);
		while (!queue.isEmpty()) {
			Node<Data> currentNode = queue.get(0);
			queue.addAll(currentNode.getChildren());
			if (currentNode.getData().getType().equals("func_dcl")) {
				if (currentNode.getChild(0).getData().getContent().contains(methodName)) {
					String timeComplexity = currentNode.getData().getTimeComplexity();
					if (timeComplexity.isEmpty()) {
						calculate(currentNode.getChild(1));
					}
					return timeComplexity;
				}
			}
			queue.remove(0);
		}
		return null;
	}

	private boolean checkRecursion(Node<Data> node) {
		Node<Data> tmpNode = node;
		while (tmpNode.getParent() != null) {
			tmpNode = tmpNode.getParent();
			if (tmpNode.getData().getType().equals("func_dcl")) {
				if (tmpNode.getChild(0).getData().getContent().contains(node.getData().getContent())) {
					tmpNode.getData().setTimeComplexity("is a recursive function");
					return true;
				}
			}
		}
		return false;
	}

	private void addFunctionRP() {
		ArrayList<Node<Data>> queue = new ArrayList<>();
		queue.add(astRoot);
		while (!queue.isEmpty()) {
			Node<Data> currentNode = queue.get(0);
			if (currentNode.getData().getType().equals("func_dcl")) {
				String timeComplexity = currentNode.getData().getTimeComplexity();
				char lastChar = timeComplexity.charAt(timeComplexity.length() - 1);
				if (lastChar == '+' || lastChar == '-') {
					timeComplexity = timeComplexity.substring(0, timeComplexity.length() - 1);
				}
				timeComplexity = addRP(timeComplexity);
				currentNode.getData().setTimeComplexity(timeComplexity);
			}
			queue.remove(0);
			queue.addAll(currentNode.getChildren());
		}
	}

	private String addRP(String timeCom) {
		int count = 0;
		for (int i = 0; i < timeCom.length(); i++) {
			if (timeCom.charAt(i) == '(')
				count++;
			else if (timeCom.charAt(i) == ')')
				count--;
		}
		if (count < 0)
			System.out.println("ERROR on RP");
		for (int i = 0; i < count; i++) {
			timeCom += ')';
		}
		return timeCom;
	}

}
