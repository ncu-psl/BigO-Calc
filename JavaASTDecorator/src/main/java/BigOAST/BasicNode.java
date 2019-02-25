package BigOAST;

import com.github.javaparser.Position;
import com.github.javaparser.ast.Node;

import java.io.Serializable;
import java.util.LinkedList;
import java.util.List;
import java.util.Optional;

public class BasicNode implements Serializable {
	private static final long serialVersionUID = 0L;
	private String _type, time_complexity = "";
	private int line_number = 0, col = 0;
	private String content = "";
	private List<BasicNode> children = new LinkedList<>();

	public BasicNode(Node jASTNode) {
		this._type = BasicNode.class.getSimpleName();
		this.setContent(jASTNode.toString());
		Optional<Position> position = jASTNode.getBegin();
		if (position.isPresent()) {
			this.setLine_number(position.get().line);
			this.setCol(position.get().column);
		}
	}

	public BasicNode(String _type, Node jASTNode) {
		this._type = _type;
		this.setContent(jASTNode.toString());
		Optional<Position> position = jASTNode.getBegin();
		if (position.isPresent()) {
			this.setLine_number(position.get().line);
			this.setCol(position.get().column);
		}
	}

	public int getLine_number() {
		return line_number;
	}

	public void setLine_number(int line_number) {
		this.line_number = line_number;
	}

	public int getCol() {
		return col;
	}

	public void setCol(int col) {
		this.col = col;
	}

	public String getType() {
		return _type;
	}

	public void setType(String _type) {
		this._type = _type;
	}

	public String getContent() {
		return content;
	}

	public void setContent(String content) {
		this.content = content;
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
