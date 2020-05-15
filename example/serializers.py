from rest_framework import serializers
import api_usuario.models


class EnderecoSerializer(serializers.ModelSerializer):
    """Cass to handle data from a Address."""

    class Meta:
        model = api_usuario.models.Endereco
        fields = ('cep', 'numero', 'endereco', 'cidade', 'uf', 'id')
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class ContatoSerializer(serializers.ModelSerializer):
    """Class to handle data from Contact."""

    class Meta:
        model = api_usuario.models.Contato
        fields = ('contato', 'id',)
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class UsuarioSerializer(serializers.ModelSerializer):
    """Class to handle Users data."""

    contatos = ContatoSerializer(many=True, required=False)
    enderecos = EnderecoSerializer(many=True, required=False)

    class Meta:
        model = api_usuario.models.Usuario
        fields = '__all__'

    def to_internal_value(self, data):
        """Clean data that may have special characters like: CPF, CEP, Phone Number.

        **Args**:
             - `data`: dados enviados.

       **Return**:
            - `Dict`: UsuarioSerializer with cleaned data.
        """
        if 'cpf' in data.keys():
            data['cpf'] = data['cpf'].replace('-', '').replace('.', '')

        if 'enderecos' in data.keys():
            for endereco in data['enderecos']:
                endereco['cep'] = endereco['cep'].replace('.', '').replace('-', '')

        if 'contatos' in data.keys():
            for contato in data['contatos']:
                characters = [' ', '(', ')', '-']
                for char in characters:
                    contato['contato'] = contato['contato'].replace(char, '')

        return super(UsuarioSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        """Custom create method to handle nested users data to be created as
        Address and Phone Number.

        **Args**:
            - `validated_data`: Dict with data field pre validated from Usuario, Contatos e Enderecos models.
        **Returns**:
            - new `User` instance just saved.
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
        """Custom updated method to handle nested users data to be updated, such as
        Address and Phone Number

        **Args**:
            - `validated_data`: Dict with data field pre validated from Usuario, Contatos e Enderecos models.
        **Returns**:
            - new `User` instance just updated.
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
        """Custom to calculate CPF digits and verify if it's a valid CPF.

        **Args**:
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
        """Perform CPF calc and valitdarion.

        **Args**:
            - `cpf`: String com o CPF

        **Returns**:
            - `True` Given CPF is valid one according to math calc.
            - `False`: Given CPF is not valid one.
        """
        primeiro_digito, segundo_digito = int(cpf[9]), int(cpf[10])
        cpf = cpf[:9]  # remover os digitos

        def calc_primeiro():
            """Verify if first digit is correct.

            **Returns**:
                - `Tuple(bool, int)`: Bool that Determinate if first digit is valid, expected match number.
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
            """Verify if second digit is correct.

            **Returns**:
                - `Tuple(bool, int)`: Bool that Determinate if second digit is valid, expected match number.
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
        """Save on database all contact instances present on a list.

        If field `id` is present:
            * if instance with given id is present on database, it is updated;
            * else instance is created with given id;

        **Args**:
            - `contatos`: List() with data to save a contact number.
            - `usuario`: model Usuario instance to be related to the contact.
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
        """Save on database all contact instances address on a list.

        If field `id` is present:
            * if instance with given id is present on database, it is updated;
            * else instance is created with given id;

        **Args**:
            - `enderecos`: List() with data to save a address.
            - `usuario`: model Usuario instance to be related to the contact.
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
