package BigOAST;

import com.github.javaparser.ast.Node;

public class CompilationUnitNode extends BasicNode {
	private static final long serialVersionUID = 0L;

	public CompilationUnitNode(Node jASTNode) {
		super(CompilationUnitNode.class.getSimpleName(), jASTNode);
	}
}
