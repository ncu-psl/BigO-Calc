package ASTGenerator;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Type;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class MyGson {
	public MyGson() {

	}

	public static String getJsonString(Node<Data> root) {
		return new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().create().toJson(root);
	}

	public static void writeJsonFile(Node<Data> root, String fileName) throws IOException {
		FileWriter fWriter = new FileWriter(new File(fileName));
		new GsonBuilder().setPrettyPrinting().create().toJson(root, fWriter);
		fWriter.close();
	}

	public static void writeJsonFile(String jsonString, String fileName) throws IOException {
		FileWriter fWriter = new FileWriter(new File(fileName));
		fWriter.write(jsonString);
		// new Gson().toJson(jsonString, fWriter);
		fWriter.close();
	}

	public static Node<Data> getDataFromJson(String jsonString, Type type) {
		return new Gson().fromJson(jsonString, type);
	}
}
