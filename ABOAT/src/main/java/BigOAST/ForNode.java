package BigOAST;

public class ForNode extends BasicNode {
	private static final long serialVersionUID = 0L;
	private String variable;
	private String init, terminal, update;

	public String getVariable() {
		return variable;
	}

	public String getInit() {
		return init;
	}

	public String getTerminal() {
		return terminal;
	}

	public String getUpdate() {
		return update;
	}

}
