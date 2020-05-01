### ContatoSerializer(serializers.ModelSerializer)
Classe para tratar dos dados de um, ou vários Contatos da API

### EnderecoSerializer(serializers.ModelSerializer)
Classe para tratar dos dados de um, ou vários Enderecos da API

### UsuarioSerializer(serializers.ModelSerializer)
Classe para tratar dos dados de um, ou vários Usuário da API

### UsuarioSerializer._calcular_cpf(cpf)
Metodo para calcular e validar os digitos do CPF


Args:

cpf: String com o CPF


Returns:

True if cpf é um cpf válido, de acordo com os calculos,
False if cpf não for válidos.


### UsuarioSerializer._calcular_cpf.calc_primeiro()
Verifica se o primeiro digito do CPF está certo


Returns:

validacão: True ou False representando se o primeiro digito
é igual ao esperado

valor_esperado: int com o resultado calculado para o
primeiro digito ser valido


### UsuarioSerializer._calcular_cpf.calc_segundo(primeiro_digito)
Verifica se o segundo digito do CPF está certo


Returns:

validacão: True ou False representando se o segundo digito
é igual ao esperado

calculo: int com o resultado calculado somatorio(digito * multiplicador)
dos digitos do cpf


### UsuarioSerializer._save_contatos(contatos, usuario)
Insere no banco de dados os contatos presente em uma lista de contatos.

Caso contenha o campo `id`:
* se existir no banco, o contato é atualizado;
* se não existir no banco é criado um novo contato com o id passado.

Caso contrário é criado um novo contato.


Args:

contatos: lista de dicionario com os campos necessarios para
salvar um endereco.
usuario: objeto da classe Usuario de api_login.Models para ser
usado na chave estrangeira.


### UsuarioSerializer._save_enderecos(enderecos, usuario)
Insere no banco de dados os enderecos presente em uma lista de enderecos.

Caso contenha o campo `id`:
* se existir no banco, o endereco é atualizado;
* se não existir no banco é criado um novo endereco com o id passado.

Caso contrário é criado um novo endereco.


Args:

enderecos: lista de dicionario com os campos necessarios para
salvar um endereco.
usuario: objeto da classe Usuario de api_login.Models para ser
usado na chave estrangeira.


### UsuarioSerializer.create(validated_data)
 Método chamado pelo método save() quando o Serializer não
possui uma instância de um api_usuario.models.Usuario (self.instace == None).

Dessa forma, sua função é salvar no banco de dados os dados
passados para o Serializer


Args:

validated_data: dicionário com os campos de um Usuario, Contatos e Enderecos pré-validados


### UsuarioSerializer.to_internal_value(data)
Metodo para limpar dados que podem chegar com caracteres especiais
como: CPF, CEP, número de telefone.


Args:

data: dados enviados

Return:
novo UsuarioSerializer com os dados limpos, sem possiveis caracteres especiais


### UsuarioSerializer.update(instance, validated_data)
 Método chamado pelo método save() quando o Serializer possui
uma instância de um api_usuario.models.Usuario (self.instace == Usuario()).

Dessa forma, sua função é atualizar o usuario no banco de dados
com os dados passados para o Serializer


Args:

validated_data: dicionário com os campos de um Usuario, Contatos e Enderecos pré-validados


### UsuarioSerializer.validate_cpf(cpf)
Metodo com todas as validacões de um CPF.


Args:

cpf: String com o CPF


Returns:

cpf com apenas digitos caso passe em todos as validações ou
raise com a mensagem de error


