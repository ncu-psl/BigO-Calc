package BigOAST;

import com.github.javaparser.Position;
import com.github.javaparser.ast.Node;

import java.io.Serializable;
import java.util.LinkedList;
import java.util.List;
import java.util.Optional;

public class BasicNode {
	private int lineNumber = 0;
	private int col = 0;
	private String type = "";
	private String Content = "";
	private List<BasicNode> children = new LinkedList<>();

	public BasicNode(Node jASTNode) {
		this.setContent(jASTNode.toString());
		Optional<Position> position = jASTNode.getBegin();
		if (position.isPresent()) {
			this.setLineNumber(position.get().line);
			this.setCol(position.get().column);
		}
	}

	public int getLineNumber() {
		return lineNumber;
	}

	public void setLineNumber(int lineNumber) {
		this.lineNumber = lineNumber;
	}

	public int getCol() {
		return col;
	}

	public void setCol(int col) {
		this.col = col;
	}

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}

	public String getContent() {
		return Content;
	}

	public void setContent(String content) {
		Content = content;
	}

	public List<BasicNode> getChildren() {
		return children;
	}

	public BasicNode getChild(int index) {
		return children.get(index);
	}

	public void setChildren(List<BasicNode> children) {
		this.children = children;
	}

	public void addChild(BasicNode newChild) {
		children.add(newChild);
	}

}
