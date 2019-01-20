package AdapterFactory;

import BigOAST.*;
import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.TypeAdapter;
import com.google.gson.reflect.TypeToken;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonWriter;

import java.io.IOException;

public class ASTNodeTypeAdapter extends TypeAdapter<BasicNode> {
	private TypeAdapter<JsonElement> jsonElementAdapter;
	private TypeAdapter<AssignNode> assignNodeTypeAdapter;
	private TypeAdapter<BasicNode> basicNodeTypeAdapter;
	private TypeAdapter<BodyNode> bodyNodeAdapter;
	private TypeAdapter<CompilationUnitNode> compilationUnitNodeTypeAdapter;
	private TypeAdapter<ForNode> forNodeTypeAdapter;
	private TypeAdapter<FunctionCallNode> functionCallNodeTypeAdapter;
	private TypeAdapter<FunctionDeclarationNode> functionDeclarationNodeTypeAdapter;
	private TypeAdapter<IFNode> ifNodeTypeAdapter;

	public ASTNodeTypeAdapter(ASTNodeAdapterFactory oldFactory, Gson gson) {
		this.jsonElementAdapter = gson.getAdapter(JsonElement.class);
		this.basicNodeTypeAdapter = gson.getDelegateAdapter(oldFactory, TypeToken.get(BasicNode.class));
		this.assignNodeTypeAdapter = gson.getDelegateAdapter(oldFactory, TypeToken.get(AssignNode.class));
		this.bodyNodeAdapter = gson.getDelegateAdapter(oldFactory, TypeToken.get(BodyNode.class));
		this.compilationUnitNodeTypeAdapter = gson.getDelegateAdapter(oldFactory, TypeToken.get(CompilationUnitNode.class));
		this.forNodeTypeAdapter = gson.getDelegateAdapter(oldFactory, TypeToken.get(ForNode.class));
		this.functionCallNodeTypeAdapter = gson.getDelegateAdapter(oldFactory, TypeToken.get(FunctionCallNode.class));
		this.functionDeclarationNodeTypeAdapter = gson.getDelegateAdapter(oldFactory, TypeToken.get(FunctionDeclarationNode.class));
		this.ifNodeTypeAdapter = gson.getDelegateAdapter(oldFactory, TypeToken.get(IFNode.class));
	}

	@Override
	public void write(JsonWriter out, BasicNode value) throws IOException {
		if (value != null) {
			if (value instanceof AssignNode) {
				assignNodeTypeAdapter.write(out, (AssignNode) value);
			} else if (value instanceof BodyNode) {
				bodyNodeAdapter.write(out, (BodyNode) value);
			} else if (value instanceof CompilationUnitNode) {
				compilationUnitNodeTypeAdapter.write(out, (CompilationUnitNode) value);
			} else if (value instanceof ForNode) {
				forNodeTypeAdapter.write(out, (ForNode) value);
			} else if (value instanceof FunctionCallNode) {
				functionCallNodeTypeAdapter.write(out, (FunctionCallNode) value);
			} else if (value instanceof FunctionDeclarationNode) {
				functionDeclarationNodeTypeAdapter.write(out, (FunctionDeclarationNode) value);
			} else if (value instanceof IFNode) {
				ifNodeTypeAdapter.write(out, (IFNode) value);
			} else {
				basicNodeTypeAdapter.write(out, value);
			}
		}
	}

	@Override
	public BasicNode read(JsonReader in) throws IOException {
		JsonObject objectJson = jsonElementAdapter.read(in).getAsJsonObject();
		JsonElement jsonElement = objectJson.get("_type");
		if (jsonElement == null) {
			return null;
		}

		String type = jsonElement.toString().replace("\"","");
		if (type.equals("AssignNode")) {
			return assignNodeTypeAdapter.fromJsonTree(objectJson);
		} else if (type.equals("BodyNode")) {
			return bodyNodeAdapter.fromJsonTree(objectJson);
		} else if (type.equals("CompilationUnitNode")) {
			return compilationUnitNodeTypeAdapter.fromJsonTree(objectJson);
		} else if (type.equals("ForNode")) {
			return forNodeTypeAdapter.fromJsonTree(objectJson);
		} else if (type.equals("FunctionCallNode")) {
			return functionCallNodeTypeAdapter.fromJsonTree(objectJson);
		} else if (type.equals("FunctionDeclarationNode")) {
			return functionDeclarationNodeTypeAdapter.fromJsonTree(objectJson);
		} else if (type.equals("IFNode")) {
			return ifNodeTypeAdapter.fromJsonTree(objectJson);
		} else {
			System.err.println("Type not found");
		}

		return null;
	}
}
