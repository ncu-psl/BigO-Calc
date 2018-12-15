package BigOAST;

import com.github.javaparser.ast.body.MethodDeclaration;

public class FunctionDeclarationNode extends FunctionNode {
	private static final long serialVersionUID = 0L;
	private String parameters;

	public FunctionDeclarationNode(MethodDeclaration node, String name, String parameters) {
		super(FunctionDeclarationNode.class.getSimpleName(), node, name);
		this.parameters = parameters;
	}

	public String getParameters() {
		return parameters;
	}

	public void setParameters(String parameters) {
		this.parameters = parameters;
	}
}
