from rest_framework import serializers
import api_usuario.models


class EnderecoSerializer(serializers.ModelSerializer):
    """Classe para tratar dos dados de um, ou vários Enderecos da API"""

    class Meta:
        model = api_usuario.models.Endereco
        fields = ('cep', 'numero', 'endereco', 'cidade', 'uf', 'id')
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class ContatoSerializer(serializers.ModelSerializer):
    """Classe para tratar dos dados de um, ou vários Contatos da API"""

    class Meta:
        model = api_usuario.models.Contato
        fields = ('contato', 'id',)
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class UsuarioSerializer(serializers.ModelSerializer):
    """Classe para tratar dos dados de um, ou vários Usuário da API"""

    contatos = ContatoSerializer(many=True, required=False)
    enderecos = EnderecoSerializer(many=True, required=False)

    class Meta:
        model = api_usuario.models.Usuario
        fields = '__all__'

    def to_internal_value(self, data):
        """Metodo para limpar dados que podem chegar com caracteres especiais
        como: CPF, CEP, número de telefone.

        Args:
             data: dados enviados

        Return:
            novo UsuarioSerializer com os dados limpos, sem possiveis caracteres especiais
        """

        if 'cpf' in data.keys():
            data['cpf'] = data['cpf'].replace('-', '')
            data['cpf'] = data['cpf'].replace('.', '')

        if 'enderecos' in data.keys():
            for endereco in data['enderecos']:
                endereco['cep'] = endereco['cep'].replace('.', '')
                endereco['cep'] = endereco['cep'].replace('-', '')

        if 'contatos' in data.keys():
            for contato in data['contatos']:
                contato['contato'] = contato['contato'].replace(' ', '')
                contato['contato'] = contato['contato'].replace('(', '')
                contato['contato'] = contato['contato'].replace(')', '')
                contato['contato'] = contato['contato'].replace('-', '')

        return super(UsuarioSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        """ Método chamado pelo método save() quando o Serializer não
        possui uma instância de um api_usuario.models.Usuario (self.instace == None).

        Dessa forma, sua função é salvar no banco de dados os dados
        passados para o Serializer

        Args:
            validated_data: dicionário com os campos de um Usuario, Contatos e Enderecos pré-validados
        """

        contatos, enderecos = [], []
        if 'contatos' in validated_data.keys():
            contatos = validated_data.pop('contatos')

        if 'enderecos' in validated_data.keys():
            enderecos = validated_data.pop('enderecos')

        usuario_novo = api_usuario.models.Usuario.objects.create(**validated_data)
        self._save_contatos(contatos, usuario_novo)
        self._save_enderecos(enderecos, usuario_novo)

        return usuario_novo

    def update(self, instance, validated_data):
        """ Método chamado pelo método save() quando o Serializer possui
        uma instância de um api_usuario.models.Usuario (self.instace == Usuario()).

        Dessa forma, sua função é atualizar o usuario no banco de dados
        com os dados passados para o Serializer

        Args:
            validated_data: dicionário com os campos de um Usuario, Contatos e Enderecos pré-validados
        """

        contatos, enderecos = [], []
        if 'contatos' in validated_data.keys():
            contatos = validated_data.pop('contatos')

        if 'enderecos' in validated_data.keys():
            enderecos = validated_data.pop('enderecos')

        usuario_dict = self.instance.__dict__
        usuario_dict.pop('_state')
        for key in validated_data.keys():
            usuario_dict[key] = validated_data[key]

        usuario = api_usuario.models.Usuario(**usuario_dict)
        usuario.save()
        self._save_contatos(contatos, usuario)
        self._save_enderecos(enderecos, usuario)
        return usuario

    def validate_cpf(self, cpf):
        """Metodo com todas as validacões de um CPF.

        Args:
            cpf: String com o CPF

        Returns:
            cpf com apenas digitos caso passe em todos as validações ou
            raise com a mensagem de error
        """

        message = None
        if len(cpf) != 11:
            message = 'cpf precisa ter 11 digitidos'
        elif not cpf.isnumeric():
            message = 'cpf tem que ser numerico.'
        elif len(cpf) != 11:
            message = 'cpf nao pode possuir mais que 11 digitos.'
        elif not self._calcular_cpf(cpf):
            message = 'cpf inválido.'

        if message is not None:
            raise serializers.ValidationError(message)
        else:
            return cpf

    def _calcular_cpf(self, cpf):
        """Metodo para calcular e validar os digitos do CPF

        Args:
            cpf: String com o CPF

        Returns:
            True if cpf é um cpf válido, de acordo com os calculos,
            False if cpf não for válidos.
        """

        primeiro_digito, segundo_digito = int(cpf[9]), int(cpf[10])
        cpf = cpf[:9]  # remover os digitos

        def calc_primeiro():
            """Verifica se o primeiro digito do CPF está certo

            Returns:
                validacão: True ou False representando se o primeiro digito
                é igual ao esperado

                valor_esperado: int com o resultado calculado para o
                primeiro digito ser valido
            """

            multiplicador = 10
            calculo = 0
            for digito in cpf:
                calculo += int(digito) * multiplicador
                multiplicador -= 1

            resto = calculo % 11
            if resto < 2:
                valor_eperado = 0
            else:
                valor_eperado = 11 - resto

            validacao = primeiro_digito == valor_eperado
            return validacao, valor_eperado

        def calc_segundo(primeiro_digito):
            """Verifica se o segundo digito do CPF está certo

            Returns:
                validacão: True ou False representando se o segundo digito
                é igual ao esperado

                calculo: int com o resultado calculado somatorio(digito * multiplicador)
                dos digitos do cpf
            """

            multiplicador = 11
            calculo = 0
            for digito in cpf:
                calculo += int(digito) * multiplicador
                multiplicador -= 1
            calculo += primeiro_digito * multiplicador

            resto = calculo % 11
            if resto < 2:
                valor_esperado = 0
            else:
                valor_esperado = 11 - resto
            validacao = segundo_digito == valor_esperado
            return validacao, calculo

        validacao_primeiro, calculo_primeiro = calc_primeiro()
        validacao_segundo, calculo_segundo = calc_segundo(calculo_primeiro)

        return validacao_primeiro and validacao_segundo

    def _save_contatos(self, contatos, usuario):
        """Insere no banco de dados os contatos presente em uma lista de contatos.

        Caso contenha o campo `id`:
            * se existir no banco, o contato é atualizado;
            * se não existir no banco é criado um novo contato com o id passado.

        Caso contrário é criado um novo contato.

        Args:
            contatos: lista de dicionario com os campos necessarios para
                salvar um endereco.
            usuario: objeto da classe Usuario de api_login.Models para ser
                usado na chave estrangeira.
        """

        for contato in contatos:
            if 'id' in contato.keys():
                try:
                    contato_objeto = api_usuario.models.Contato.objects.get(id=contato['id'])
                except api_usuario.models.Contato.DoesNotExist:
                    continue

                if contato_objeto.usuario.id != usuario.id:
                    # verificar se o contato pertence ao usuário que esta pretendendo alterar
                    continue

            contato = api_usuario.models.Contato(**contato, usuario=usuario)
            contato.save()

    def _save_enderecos(self, enderecos, usuario):
        """Insere no banco de dados os enderecos presente em uma lista de enderecos.

        Caso contenha o campo `id`:
            * se existir no banco, o endereco é atualizado;
            * se não existir no banco é criado um novo endereco com o id passado.

        Caso contrário é criado um novo endereco.

        Args:
            enderecos: lista de dicionario com os campos necessarios para
                salvar um endereco.
            usuario: objeto da classe Usuario de api_login.Models para ser
                usado na chave estrangeira.
        """

        for endereco in enderecos:
            if 'id' in endereco.keys():  # tentando atualizar um endereco
                try:
                    endereco_objeto = api_usuario.models.Endereco.objects.get(id=endereco['id'])
                except api_usuario.models.Contato.DoesNotExist:
                    continue

                if endereco_objeto.usuario.id != usuario.id:
                    # verificar se o contato pertence ao usuário que esta pretendendo alterar
                    continue

            endereco = api_usuario.models.Endereco(**endereco, usuario=usuario)
            endereco.save()