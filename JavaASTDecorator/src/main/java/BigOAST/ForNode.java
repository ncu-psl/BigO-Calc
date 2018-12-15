package BigOAST;

import com.github.javaparser.ast.Node;

public class ForNode extends BasicNode {
	private static final long serialVersionUID = 0L;
	private String variable;
	private String init, terminal, update;

	public ForNode(Node node, String variable, String init, String terminal, String update) {
		super(ForNode.class.getSimpleName(), node);
		this.variable = variable;
		this.init = init;
		this.terminal = terminal;
		this.update = update;
	}

	public String getVariable() {
		return variable;
	}

	public void setVariable(String variable) {
		this.variable = variable;
	}

	public String getInit() {
		return init;
	}

	public void setInit(String init) {
		this.init = init;
	}

	public String getTerminal() {
		return terminal;
	}

	public void setTerminal(String terminal) {
		this.terminal = terminal;
	}

	public String getUpdate() {
		return update;
	}

	public void setUpdate(String update) {
		this.update = update;
	}

}
