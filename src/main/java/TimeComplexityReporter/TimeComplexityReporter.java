package TimeComplexityReporter;

import ASTGenerator.Data;
import ASTGenerator.MyGson;
import ASTGenerator.Node;
import com.google.gson.reflect.TypeToken;

import java.util.ArrayList;

public class TimeComplexityReporter {
	Node<Data> astRoot;

	public TimeComplexityReporter(String jsonString) {
		this.astRoot = MyGson.getDataFromJson(jsonString, new TypeToken<Node<Data>>() {
		}.getType());
		dfsSetParent(astRoot);
	}

	private void dfsSetParent(Node<Data> currentNode) {
		for (Node<Data> childNode : currentNode.getChildren()) {
			childNode.setParent(currentNode);
			dfsSetParent(childNode);
		}
	}

	public String report() {
		String string;
		ArrayList<Node<Data>> queue = new ArrayList<>();
		queue.add(astRoot);
		string = "[Time complexity]\n";
		while (!queue.isEmpty()) {
			Node<Data> currentNode = queue.get(0);
			queue.addAll(currentNode.getChildren());
			if (currentNode.getData().getType().equals("func_dcl")) {
				String timeComplexity = "";
				for (Node<Data> child : currentNode.getChildren()) {
					if (child.getData().getType().equals("func_name")) {
						timeComplexity = currentNode.getData().getTimeComplexity();
						if (!timeComplexity.equals("is a recursive function")) {
							timeComplexity = timeComplexity.substring(0, timeComplexity.length() - 1);
						}
						timeComplexity = addRP(timeComplexity);
					}
				}
				string += currentNode.getChild(0).getData().getContent() + " = " + timeComplexity + "\n";
			}
			queue.remove(0);
		}
		string += "\n[Dependency]\n";
		string += getFunctionCallDependency();
		return string;
	}

	private String getFunctionCallDependency() {
		String string = "";
		ArrayList<Node<Data>> queue = new ArrayList<>();
		queue.add(astRoot);
		while (!queue.isEmpty()) {
			Node<Data> currentNode = queue.get(0);
			queue.addAll(currentNode.getChildren());
			if (currentNode.getData().getType().equals("func_call")) {
				Node<Data> parentNode = currentNode;
				while (!parentNode.getData().getType().equals("func_dcl")) {
					parentNode = parentNode.getParent();
				}

				if (parentNode.getData().getType().equals("func_dcl")) {
					for (Node<Data> child : parentNode.getChildren()) {
						if (child.getData().getType().equals("func_name")) {
							if (!parentNode.getData().getTimeComplexity().equals("is a recursive function")) {
								string += child.getData().getContent() + " call " + currentNode.getData().getContent() + "\n";
							}
						}
					}
				}
			}
			queue.remove(0);
		}
		return string;
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
