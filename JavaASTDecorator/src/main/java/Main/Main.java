package Main;

import ASTDecorator.ASTDecorator;
import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.serialization.JavaParserJsonSerializer;

import java.io.FileInputStream;
import java.io.FileNotFoundException;

public class Main {

	public static void main(String[] args) throws FileNotFoundException {
		FileInputStream in = new FileInputStream("./src/main/resources/For.java");
		CompilationUnit cu = JavaParser.parse(in);

		JavaParserJsonSerializer jsonSerializer = new JavaParserJsonSerializer();
		JsonOutputUtils.toJson(cu, "./src/main/resources/tree.json");

		try {
			ASTDecorator astDecorator = new ASTDecorator();
			astDecorator.decorate(cu);
		} catch (Exception exception) {
			exception.printStackTrace();
		}
	}

}
