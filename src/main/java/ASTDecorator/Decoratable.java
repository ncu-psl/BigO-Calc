package ASTDecorator;

import ASTGenerator.Data;
import ASTGenerator.Node;

public interface Decoratable {
	void decorateForNode(Node<Data> currentNode);

	void decorateFunctionDeclaration(Node<Data> currentNode);

	void decorateFunctionCall(Node<Data> currentNode);

	void decorateAssignment(Node<Data> currentNode);
}
