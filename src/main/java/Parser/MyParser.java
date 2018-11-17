package Parser;

import org.antlr.v4.runtime.Parser;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.atn.ATN;

public class MyParser extends Parser implements IStartable {

	public MyParser(TokenStream input) {
		super(input);
	}

	@Override
	public ATN getATN() {
		return null;
	}

	@Override
	public String getGrammarFileName() {
		return null;
	}

	@Override
	public String[] getRuleNames() {
		return null;
	}

	@Override
	public String[] getTokenNames() {
		return null;
	}

	@Override
	public ParserRuleContext getParserRuleContext() {
		return null;
	}

}
