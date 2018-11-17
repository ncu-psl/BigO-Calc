package Factory;

import ASTDecorator.ASTDecorator;
import ASTDecorator.CASTDecorator;
import ASTDecorator.CPP14ASTDecorator;
import ASTDecorator.Java8ASTDecorator;
import Main.Language;

public class ASTDecoratorFactory {
	public static ASTDecorator create(Language language, String astJsonString) throws UnknownLanguageException {
		switch (language) {
			case C:
				return new CASTDecorator(astJsonString);
			case CPP14:
				return new CPP14ASTDecorator(astJsonString);
			/*
			 * case "f": case "f77": case "f90": throw new unknow break;
			 */
			case JAVA8:
				return new Java8ASTDecorator(astJsonString);
			default:
				throw new UnknownLanguageException();
		}
	}
}
