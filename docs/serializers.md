### ContatoSerializer(serializers.ModelSerializer)
Classe para tratar dos dados de um, ou v�rios Contatos da API

### EnderecoSerializer(serializers.ModelSerializer)
Classe para tratar dos dados de um, ou v�rios Enderecos da API

### UsuarioSerializer(serializers.ModelSerializer)
Classe para tratar dos dados de um, ou v�rios Usu�rio da API

### UsuarioSerializer._calcular_cpf(cpf)
Metodo para calcular e validar os digitos do CPF


Args:

cpf: String com o CPF


Returns:

True if cpf � um cpf v�lido, de acordo com os calculos,
False if cpf n�o for v�lidos.


### UsuarioSerializer._calcular_cpf.calc_primeiro()
Verifica se o primeiro digito do CPF est� certo


Returns:

validac�o: True ou False representando se o primeiro digito
� igual ao esperado

valor_esperado: int com o resultado calculado para o
primeiro digito ser valido


### UsuarioSerializer._calcular_cpf.calc_segundo(primeiro_digito)
Verifica se o segundo digito do CPF est� certo


Returns:

validac�o: True ou False representando se o segundo digito
� igual ao esperado

calculo: int com o resultado calculado somatorio(digito * multiplicador)
dos digitos do cpf


### UsuarioSerializer._save_contatos(contatos, usuario)
Insere no banco de dados os contatos presente em uma lista de contatos.

Caso contenha o campo `id`:
* se existir no banco, o contato � atualizado;
* se n�o existir no banco � criado um novo contato com o id passado.

Caso contr�rio � criado um novo contato.


Args:

contatos: lista de dicionario com os campos necessarios para
salvar um endereco.
usuario: objeto da classe Usuario de api_login.Models para ser
usado na chave estrangeira.


### UsuarioSerializer._save_enderecos(enderecos, usuario)
Insere no banco de dados os enderecos presente em uma lista de enderecos.

Caso contenha o campo `id`:
* se existir no banco, o endereco � atualizado;
* se n�o existir no banco � criado um novo endereco com o id passado.

Caso contr�rio � criado um novo endereco.


Args:

enderecos: lista de dicionario com os campos necessarios para
salvar um endereco.
usuario: objeto da classe Usuario de api_login.Models para ser
usado na chave estrangeira.


### UsuarioSerializer.create(validated_data)
 M�todo chamado pelo m�todo save() quando o Serializer n�o
possui uma inst�ncia de um api_usuario.models.Usuario (self.instace == None).

Dessa forma, sua fun��o � salvar no banco de dados os dados
passados para o Serializer


Args:

validated_data: dicion�rio com os campos de um Usuario, Contatos e Enderecos pr�-validados


### UsuarioSerializer.to_internal_value(data)
Metodo para limpar dados que podem chegar com caracteres especiais
como: CPF, CEP, n�mero de telefone.


Args:

data: dados enviados

Return:
novo UsuarioSerializer com os dados limpos, sem possiveis caracteres especiais


### UsuarioSerializer.update(instance, validated_data)
 M�todo chamado pelo m�todo save() quando o Serializer possui
uma inst�ncia de um api_usuario.models.Usuario (self.instace == Usuario()).

Dessa forma, sua fun��o � atualizar o usuario no banco de dados
com os dados passados para o Serializer


Args:

validated_data: dicion�rio com os campos de um Usuario, Contatos e Enderecos pr�-validados


### UsuarioSerializer.validate_cpf(cpf)
Metodo com todas as validac�es de um CPF.


Args:

cpf: String com o CPF


Returns:

cpf com apenas digitos caso passe em todos as valida��es ou
raise com a mensagem de error


