package Factory;

import java.io.IOException;
import java.nio.file.Paths;

import Main.Language;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.Lexer;

import C.CLexer;
import CPP14.CPP14Lexer;
import Java8.Java8Lexer;

public class LexerFactory {

	public static Lexer create(Language language, String fileName) throws UnknownLanguageException, IOException {
		CharStream charStream = CharStreams.fromPath(Paths.get(fileName));
		switch (language) {
			case C:
				return new CLexer(charStream);
			case CPP14:
				return new CPP14Lexer(charStream);
			/*
			 * case "f": case "f77": case "f90": throw new unknow break;
			 */
			case JAVA8:
				return new Java8Lexer(charStream);
			default:
				throw new UnknownLanguageException();
		}
	}

}
