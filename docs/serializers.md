### ContatoSerializer(serializers.ModelSerializer)
Class to handle data from Contact.

### EnderecoSerializer(serializers.ModelSerializer)
Cass to handle data from a Address.

### UsuarioSerializer(serializers.ModelSerializer)
Class to handle Users data.

### UsuarioSerializer._calcular_cpf(cpf)
Perform CPF calc and valitdarion.

**Args**:
- `cpf`: String com o CPF

**Returns**:
- `True` Given CPF is valid one according to math calc.
- `False`: Given CPF is not valid one.


### UsuarioSerializer._calcular_cpf.calc_primeiro()
Verify if first digit is correct.

**Returns**:
- `Tuple(bool, int)`: Bool that Determinate if first digit is valid, expected match number.


### UsuarioSerializer._calcular_cpf.calc_segundo(primeiro_digito)
Verify if second digit is correct.

**Returns**:
- `Tuple(bool, int)`: Bool that Determinate if second digit is valid, expected match number.


### UsuarioSerializer._save_contatos(contatos, usuario)
Save on database all contact instances present on a list.

If field `id` is present:
* if instance with given id is present on database, it is updated;
* else instance is created with given id;

**Args**:
- `contatos`: List() with data to save a contact number.
- `usuario`: model Usuario instance to be related to the contact.


### UsuarioSerializer._save_enderecos(enderecos, usuario)
Save on database all contact instances address on a list.

If field `id` is present:
* if instance with given id is present on database, it is updated;
* else instance is created with given id;

**Args**:
- `enderecos`: List() with data to save a address.
- `usuario`: model Usuario instance to be related to the contact.


### UsuarioSerializer.create(validated_data)
Custom create method to handle nested users data to be created as
Address and Phone Number.

**Args**:
- `validated_data`: Dict with data field pre validated from Usuario, Contatos e Enderecos models.
**Returns**:
- new `User` instance just saved.


### UsuarioSerializer.to_internal_value(data)
Clean data that may have special characters like: CPF, CEP, Phone Number.

**Args**:
- `data`: dados enviados.

**Return**:
- `Dict`: UsuarioSerializer with cleaned data.


### UsuarioSerializer.update(instance, validated_data)
Custom updated method to handle nested users data to be updated, such as
Address and Phone Number

**Args**:
- `validated_data`: Dict with data field pre validated from Usuario, Contatos e Enderecos models.
**Returns**:
- new `User` instance just updated.


### UsuarioSerializer.validate_cpf(cpf)
Custom to calculate CPF digits and verify if it's a valid CPF.

**Args**:
cpf: String com o CPF


Returns:

cpf com apenas digitos caso passe em todos as validações ou
raise com a mensagem de error


