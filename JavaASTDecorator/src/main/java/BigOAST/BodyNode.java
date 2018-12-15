package BigOAST;

import com.github.javaparser.ast.Node;

public class BodyNode extends BasicNode {
	private static final long serialVersionUID = 0L;

	public BodyNode(Node jASTNode) {
		super(BodyNode.class.getSimpleName(), jASTNode);
	}
}
