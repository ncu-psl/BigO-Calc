package BigOAST;

import com.github.javaparser.ast.Node;

public class IFNode extends BasicNode {
	private static final long serialVersionUID = 0L;

	public IFNode(Node jASTNode) {
		super(IFNode.class.getSimpleName(), jASTNode);
	}
}
