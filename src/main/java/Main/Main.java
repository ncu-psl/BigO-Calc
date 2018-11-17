package Main;

import ASTDecorator.ASTDecorator;
import ASTGenerator.ASTGenerator;
import ASTGenerator.MyGson;
import ASTGenerator.TimeComplexityCalculator;
import Factory.ASTDecoratorFactory;
import Factory.UnknownLanguageException;
import TimeComplexityReporter.TimeComplexityReporter;
import com.google.gson.JsonIOException;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Properties;

public class Main {

	public static void main(String args[]) throws IOException, UnknownLanguageException, JsonIOException {
		//System.out.println("Working Directory = " + System.getProperty("user.dir"));
		Properties properties = new Properties();
		try {
			properties.load(new FileInputStream("./src/main/resources/config.properties"));
		} catch (Exception e) {
			e.printStackTrace();
		}
		boolean printDot = Boolean.valueOf(properties.getProperty("printDot"));
		boolean printAST = Boolean.valueOf(properties.getProperty("printAST"));
		boolean verbose = Boolean.valueOf(properties.getProperty("verbose"));
		String inputFile = properties.getProperty("inputFile");
		String BigOReportFile = properties.getProperty("BigOReportFile");

		Language language = Language.valueOf(properties.getProperty("language").toUpperCase());

		String ASTJsonFile = properties.getProperty("ASTJsonFile");
		ASTGenerator astGenerator = new ASTGenerator(language, inputFile);
		astGenerator.setPrintAST(printAST);
		astGenerator.setPrintDot(printDot);
		astGenerator.setVerbose(verbose);
		String astJsonString = astGenerator.generateAST();
		MyGson.writeJsonFile(astJsonString, ASTJsonFile);

		System.err.println();

		String decoratedJsonFile = properties.getProperty("decoratedJsonFile");
		ASTDecorator astDecorator = ASTDecoratorFactory.create(language, astJsonString);
		String decoratedASTJsonString = astDecorator.decorate();
		MyGson.writeJsonFile(decoratedASTJsonString, decoratedJsonFile);

		String bigOJsonFile = properties.getProperty("bigOJsonFile");
		TimeComplexityCalculator calculator = new TimeComplexityCalculator();
		calculator.setAstRoot(decoratedASTJsonString);
		String bigOJsonString = calculator.calculate();
		MyGson.writeJsonFile(bigOJsonString, bigOJsonFile);

		TimeComplexityReporter reporter = new TimeComplexityReporter(bigOJsonString);
		String bigOReport = reporter.report();
		FileWriter fileWriter = new FileWriter(new File(BigOReportFile));
		fileWriter.write(bigOReport);
		fileWriter.close();
		System.out.println(bigOReport);
	}
}
