package BigOAST;

import com.github.javaparser.ast.Node;

public abstract class FunctionNode extends BasicNode {
	private static final long serialVersionUID = 0L;
	private String name;
	private boolean recursive = false;

	public FunctionNode(String _type, Node jASTNode, String name) {
		super(_type, jASTNode);
		this.setName(name);
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public boolean isRecursive() {
		return recursive;
	}
}
