package BigOAST;


public class AssignNode extends BasicNode {
	private static final long serialVersionUID = 0L;
	private BasicNode leftNode;
	private BasicNode rightNode;

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
