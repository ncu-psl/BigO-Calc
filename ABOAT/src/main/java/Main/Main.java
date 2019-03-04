package Main;

import AdapterFactory.ASTNodeAdapterFactory;
import BigOAST.BasicNode;
import BigOAST.CompilationUnitNode;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.FileWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
	public static void main(String[] args) {
		Gson gson = new GsonBuilder().setPrettyPrinting().disableHtmlEscaping()
				.registerTypeAdapterFactory(new ASTNodeAdapterFactory()).create();

		try {
			Path path = Paths.get("./src/main/resources/big-o ast.json");
			String jsonString = new String(Files.readAllBytes(path));
			BasicNode cu = gson.fromJson(jsonString, BasicNode.class);

			// calculate Big-O
			TimeComplexityCalculator tcc = new TimeComplexityCalculator();
			tcc.calculate((CompilationUnitNode) cu);

			// dump json file
			FileWriter fw = new FileWriter("./src/main/resources/big-o ast with time complexity.json");
			gson.toJson(cu, fw);
			fw.close();
		} catch (Exception ex) {
			ex.printStackTrace();
		}

	}
}
