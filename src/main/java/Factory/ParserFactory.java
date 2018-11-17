package Factory;

import Main.Language;
import org.antlr.v4.runtime.TokenStream;

import C.CParser;
import CPP14.CPP14Parser;
import Java8.Java8Parser;
import Parser.MyParser;

public class ParserFactory {
	public static MyParser create(Language language, TokenStream tokenStream) throws UnknownLanguageException {
		switch (language) {
			case C:
				return new CParser(tokenStream);
			case CPP14:
				return new CPP14Parser(tokenStream);
			/*
			 * case "f": case "f77": case "f90": throw new unknown break;
			 */
			case JAVA8:
				return new Java8Parser(tokenStream);
			default:
				throw new UnknownLanguageException();
		}
	}
}
