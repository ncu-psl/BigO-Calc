package ASTDecorator;

import BigOAST.*;
import Main.ForMultipleInitializationException;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.*;
import com.github.javaparser.ast.stmt.BlockStmt;
import com.github.javaparser.ast.stmt.ForStmt;
import com.github.javaparser.ast.stmt.Statement;

import java.util.List;
import java.util.Optional;

public class ASTDecorator {

	public CompilationUnitNode decorate(CompilationUnit jASTcu) {
		CompilationUnitNode cu = new CompilationUnitNode(jASTcu);
		cu.setContent(jASTcu.toString());
		try {
			decorate(jASTcu, cu);
		} catch (Exception ex) {
			ex.printStackTrace();
		}
		return cu;
	}

	private void decorate(Node jASTNode, BasicNode parentNode) throws ForMultipleInitializationException {
		BasicNode currentNode;
		if (jASTNode instanceof MethodDeclaration) {
			currentNode = decorateMethodDeclaration((MethodDeclaration) jASTNode);
			Optional<BlockStmt> blockStmt = ((MethodDeclaration) jASTNode).getBody();
			if (blockStmt.isPresent()) {
				for (Node node : blockStmt.get().getStatements()) {
					decorate(node, currentNode);
				}
			}
		} else if (jASTNode instanceof MethodCallExpr) {
			currentNode = decorateFunctionCall((MethodCallExpr) jASTNode);
		} else if (jASTNode instanceof AssignExpr) {
			currentNode = decorateAssignment((AssignExpr) jASTNode);
		} else if (jASTNode instanceof ForStmt) {
			currentNode = decorateForNode((ForStmt) jASTNode);
			Statement statement = ((ForStmt) jASTNode).getBody();
			if (statement instanceof BlockStmt) {
				BlockStmt blockStmt = ((BlockStmt) statement);
				for (Node node : blockStmt.getStatements()) {
					decorate(node, currentNode);
				}
			}
		} else if (jASTNode instanceof BlockStmt) {
			currentNode = decorateBodyNode((BlockStmt) jASTNode);
			for (Node node : jASTNode.getChildNodes()) {
				decorate(node, currentNode);
			}
		} else {
			currentNode = decorateOtherNode(jASTNode);
			for (Node node : jASTNode.getChildNodes()) {
				decorate(node, currentNode);
			}
		}
		parentNode.addChild(currentNode);
	}

	private ForNode decorateForNode(ForStmt forStmt) throws ForMultipleInitializationException {
		List<Expression> initList = forStmt.getInitialization();
		if (initList.size() > 1) {
			throw new ForMultipleInitializationException();
		}

		Expression initExpr = initList.get(0);
		String variable = ((AssignExpr) initExpr).getTarget().toString();
		String init = ((AssignExpr) initExpr).getValue().toString();

		String comp = "";
		if (forStmt.getCompare().isPresent()) {
			Expression compareExpr = forStmt.getCompare().get();
			comp = ((BinaryExpr) compareExpr).getRight().toString();
		}

		String update = "";
		List<Expression> updateList = forStmt.getUpdate();
		if (updateList.size() > 1) {
			throw new ForMultipleInitializationException();
		}
		UnaryExpr.Operator opr = ((UnaryExpr) updateList.get(0)).getOperator();
		if (opr.equals(UnaryExpr.Operator.PREFIX_INCREMENT) || (opr.equals(UnaryExpr.Operator.POSTFIX_INCREMENT))) {
			update = "+1";
		} else if (opr.equals(UnaryExpr.Operator.PREFIX_DECREMENT) || (opr.equals(UnaryExpr.Operator.POSTFIX_DECREMENT))) {
			update = "-1";
		}

		ForNode forNode = new ForNode(forStmt, variable, init, comp, update);
		return forNode;
	}

	private FunctionDeclarationNode decorateMethodDeclaration(MethodDeclaration methodDeclaration) {
		String name = methodDeclaration.getName().asString();
		String parameter = methodDeclaration.getParameters().toString();
		FunctionDeclarationNode functionDeclarationNode = new FunctionDeclarationNode(methodDeclaration, name, parameter);
		return functionDeclarationNode;
	}

	private FunctionCallNode decorateFunctionCall(MethodCallExpr methodCallExpr) {
		String name = methodCallExpr.getName().asString();
		String parameter = methodCallExpr.getArguments().toString();
		FunctionCallNode functionCallNode = new FunctionCallNode(methodCallExpr, name, parameter);
		return functionCallNode;
	}

	private AssignNode decorateAssignment(AssignExpr assignExpr) {
		Expression leftExpr = (assignExpr).getTarget();
		Expression rightExpr = (assignExpr).getValue();
		BasicNode leftNode = new BasicNode(leftExpr), rightNode = new BasicNode(rightExpr);

		AssignNode assignNode = new AssignNode(assignExpr, leftNode, rightNode);
		return assignNode;
	}

	private BasicNode decorateOtherNode(Node otherNode) {
		BasicNode basicNode = new BasicNode(otherNode);
		return basicNode;
	}

	private BodyNode decorateBodyNode(BlockStmt bodyStmt) {
		BodyNode bodyNode = new BodyNode(bodyStmt);
		return bodyNode;
	}

}
