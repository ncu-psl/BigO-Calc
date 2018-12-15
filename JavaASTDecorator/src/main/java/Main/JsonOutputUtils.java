package Main;

import BigOAST.BasicNode;
import com.github.javaparser.ast.Node;
import com.github.javaparser.printer.JsonPrinter;
import com.google.gson.GsonBuilder;

import java.io.File;
import java.io.FileWriter;

public class JsonOutputUtils {
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
		String json = new GsonBuilder().setPrettyPrinting().create().toJson(node);
		return json;
	}

	public static String toJson(BasicNode node, String path) {
		String json = toJson(node);
		toFile(json, path);
		return json;
	}
}
