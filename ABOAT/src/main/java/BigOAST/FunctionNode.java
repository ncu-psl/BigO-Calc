package BigOAST;

public class FunctionNode extends BasicNode {
	private static final long serialVersionUID = 0L;
	private String name;
	private boolean recursive = false;

	public String getName() {
		return name;
	}

	public boolean isRecursive() {
		return recursive;
	}

	public void setRecursive(boolean recursive) {
		this.recursive = recursive;
	}
}
