package BigOAST;

import com.github.javaparser.ast.Node;

public class IFNode extends BasicNode {
	public IFNode(Node jASTNode) {
		super(IFNode.class.getSimpleName(), jASTNode);
	}
}
