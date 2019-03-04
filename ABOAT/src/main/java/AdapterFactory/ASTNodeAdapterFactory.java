package AdapterFactory;

import BigOAST.BasicNode;
import com.google.gson.Gson;
import com.google.gson.TypeAdapter;
import com.google.gson.TypeAdapterFactory;
import com.google.gson.reflect.TypeToken;

public class ASTNodeAdapterFactory implements TypeAdapterFactory {

	@Override
	@SuppressWarnings("unchecked")
	public <T> TypeAdapter<T> create(Gson gson, TypeToken<T> type) {
		if (!BasicNode.class.isAssignableFrom(type.getRawType())) {
			return null;
		}
		return (TypeAdapter<T>) new ASTNodeTypeAdapter(this, gson).nullSafe();
	}
}
