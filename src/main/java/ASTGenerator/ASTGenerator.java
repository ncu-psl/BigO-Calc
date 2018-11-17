package ASTGenerator;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;

import Main.Language;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.RuleContext;
import org.antlr.v4.runtime.tree.ParseTree;

import Factory.LexerFactory;
import Factory.ParserFactory;
import Factory.UnknownLanguageException;

import Parser.MyParser;

public class ASTGenerator {
	private String fileName;
	private Language language;
	private boolean printAST = false, printDot = false, verbose = false;

	private static ArrayList<String> LineNum = new ArrayList<>();
	private static ArrayList<String> Type = new ArrayList<>();
	private static ArrayList<String> Content = new ArrayList<>();
	private static ArrayList<String> ruleNames = new ArrayList<>();

	public ASTGenerator(Language language, String fileName) {
		this.fileName = fileName;
		this.language = language;
	}

	public String generateAST() throws IOException, UnknownLanguageException {
		Lexer lexer = LexerFactory.create(language, fileName);
		CommonTokenStream tokens = new CommonTokenStream(lexer);
		MyParser parser = ParserFactory.create(language, tokens);
		ParserRuleContext ctx = parser.getParserRuleContext();
		ruleNames = new ArrayList<>(Arrays.asList(parser.getRuleNames()));
		Node<Data> root = new Node<Data>();
		generateAST(ctx, 0, root);
		String jsonString = MyGson.getJsonString(root);
		if (printAST) {
			System.out.print(jsonString);
		}

		String dotString = printDOT();
		if (printDot) {
			System.out.print(dotString);
		}
		return jsonString;
	}

	private void generateAST(RuleContext ctx, int indentation, Node<Data> node) {
		boolean toBeIgnore = !verbose && ctx.getChildCount() == 1 && ctx.getChild(0) instanceof ParserRuleContext;

		if (!toBeIgnore) {
			String ruleName = ruleNames.get(ctx.getRuleIndex());
			LineNum.add(Integer.toString(indentation));
			Type.add(ruleName);
			Content.add(ctx.getText());
			node.setData(new Data(indentation + "", ruleName, ctx.getText()));
		}

		for (int i = 0; i < ctx.getChildCount(); i++) {
			ParseTree element = ctx.getChild(i);
			if (element instanceof RuleContext) {
				Node<Data> child = new Node<>(new Data());
				generateAST((RuleContext) element, indentation + (toBeIgnore ? 0 : 1), child);
				node.addChild(child);
			}
		}
	}

	public void setPrintAST(boolean printAST) {
		this.printAST = printAST;
	}

	public void setPrintDot(boolean printDot) {
		this.printDot = printDot;
	}

	public void setVerbose(boolean verbose) {
		this.verbose = verbose;
	}

	private static String printDOT() throws IOException {
		StringBuffer str = new StringBuffer();
		str.append("digraph G {\n");
		printLabel(str);
		for (int i = 1; i < LineNum.size(); i++) {
			int line = Integer.parseInt(LineNum.get(i)) - 1;
			int pos = getPos(line, i);
			if (pos == -1) {
				str.append("LineNum: ");
				str.append(line);
				str.append(" not found!");
			}
			str.append(line).append(pos).append("->");
			str.append(LineNum.get(i)).append(i).append("\n");
		}
		str.append("}\n");
		FileWriter fileWriter = new FileWriter(new File("output.dot"));
		fileWriter.write(str.toString());
		fileWriter.close();
		return str.toString();
	}

	private static void printLabel(StringBuffer str) {
		for (int i = 0; i < LineNum.size(); i++) {
			str.append(LineNum.get(i)).append(i);
			str.append("[label=\"").append(Type.get(i)).append("\\n ");
			str.append(Content.get(i)).append(" \"]\n");
		}
	}

	private static int getPos(int n, int limit) {
		for (int pos = limit - 1; pos >= 0; pos--) {
			if (Integer.parseInt(LineNum.get(pos)) == n) {
				return pos;
			}
		}
		return -1;
	}

}
