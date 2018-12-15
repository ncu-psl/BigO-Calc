package BigOAST;

import com.github.javaparser.ast.expr.MethodCallExpr;

public class FunctionCallNode extends FunctionNode {
	private static final long serialVersionUID = 0L;
	private String arguments;

	public FunctionCallNode(MethodCallExpr node, String name, String arguments) {
		super(FunctionCallNode.class.getSimpleName(), node, name);
		this.arguments = arguments;
	}

	public String getArguments() {
		return arguments;
	}

	public void setArguments(String arguments) {
		this.arguments = arguments;
	}
}
