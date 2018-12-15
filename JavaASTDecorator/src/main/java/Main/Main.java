package Main;

import ASTDecorator.ASTDecorator;
import BigOAST.BasicNode;
import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.serialization.JavaParserJsonSerializer;

import java.io.FileInputStream;
import java.io.FileNotFoundException;

public class Main {

	public static void main(String[] args) throws FileNotFoundException {
		FileInputStream in = new FileInputStream("./src/main/resources/For.java");
		CompilationUnit jASTcu = JavaParser.parse(in);

		JavaParserJsonSerializer jsonSerializer = new JavaParserJsonSerializer();
		JsonOutputUtils.toJson(jASTcu, "./src/main/resources/tree.json");

		try {
			// decorate JavaParser AST to Big-O AST
			ASTDecorator astDecorator = new ASTDecorator();
			BasicNode cu = astDecorator.decorate(jASTcu);

			// write Json File
			JsonOutputUtils.toJson(cu, "./src/main/resources/big-o ast.json");
		} catch (Exception exception) {
			exception.printStackTrace();
		}
	}

}
