package ASTGenerator;

public class Data {
	private String lineNum = "";
	private String type = "";
	private String content = "";
	private String timeComplexity = "";

	public Data() {

	}

	public Data(String lineNum, String type, String content) {
		this.lineNum = lineNum;
		this.type = type;
		this.content = content;
	}

	public String getLineNum() {
		return lineNum;
	}

	public void setLineNum(String lineNum) {
		this.lineNum = lineNum;
	}

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}

	public String getContent() {
		return content;
	}

	public void setContent(String content) {
		this.content = content;
	}

	public String getTimeComplexity() {
		return timeComplexity;
	}

	public void setTimeComplexity(String timeComplexity) {
		this.timeComplexity = timeComplexity;
	}

}
