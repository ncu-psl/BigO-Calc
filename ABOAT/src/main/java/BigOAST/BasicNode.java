package BigOAST;

import java.io.Serializable;
import java.util.LinkedList;
import java.util.List;

public class BasicNode implements Serializable {
	private static final long serialVersionUID = 0L;
	private String _type, TimeComplexity = "";
	private int lineNumber = 0, col = 0;
	private String Content = "";
	private List<BasicNode> children = new LinkedList<>();

	public String getType() {
		return _type;
	}

	public String getTimeComplexity() {
		return TimeComplexity;
	}

	public void setTimeComplexity(String timeComplexity) {
		TimeComplexity = timeComplexity;
	}

	public int getLineNumber() {
		return lineNumber;
	}

	public int getCol() {
		return col;
	}

	public String getContent() {
		return Content;
	}

	public List<BasicNode> getChildren() {
		return children;
	}

	public BasicNode getChild(int index) {
		return children.get(index);
	}

}
