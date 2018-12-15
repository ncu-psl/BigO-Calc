package BigOAST;

import com.github.javaparser.ast.Node;

public class AssignNode extends BasicNode {
	private static final long serialVersionUID = 0L;
	private BasicNode leftNode;
	private BasicNode rightNode;

	public AssignNode(Node jASTNode, BasicNode leftNode, BasicNode rightNode) {
		super(AssignNode.class.getSimpleName(), jASTNode);
		this.setLeftNode(leftNode);
		this.setRightNode(rightNode);
	}

	public BasicNode getLeftNode() {
		return leftNode;
	}

	public void setLeftNode(BasicNode leftNode) {
		this.leftNode = leftNode;
	}

	public BasicNode getRightNode() {
		return rightNode;
	}

	public void setRightNode(BasicNode rightNode) {
		this.rightNode = rightNode;
	}

}
