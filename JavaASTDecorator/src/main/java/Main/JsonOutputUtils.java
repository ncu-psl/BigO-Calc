package Main;

import AdapterFactory.ASTNodeAdapterFactory;
import BigOAST.BasicNode;
import com.github.javaparser.ast.Node;
import com.github.javaparser.printer.JsonPrinter;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.File;
import java.io.FileWriter;

public class JsonOutputUtils {
	private static Gson gson = new GsonBuilder().setPrettyPrinting().disableHtmlEscaping()
			.registerTypeAdapterFactory(new ASTNodeAdapterFactory()).create();

	public static void toFile(String json, String path) {
		try {
			FileWriter fWriter = new FileWriter(new File(path));
			fWriter.write(json);
			fWriter.close();
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}

	public static String toJson(Node node) {
		String json = new JsonPrinter(true).output(node);
		return json;
	}

	public static String toJson(Node node, String path) {
		String json = toJson(node);
		toFile(json, path);
		return json;
	}

	public static String toJson(BasicNode node) {
		String json = gson.toJson(node);
		return json;
	}

	public static String toJson(BasicNode node, String path) {
		String json = toJson(node);
		toFile(json, path);
		return json;
	}
}
