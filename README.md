# Generate makdown from .py files

Script para gerar markdown dos arquivos python.

## How to use

Cole o arquivo `generate.py` **na raiz** do projeto e altere as variáveis seguintes variáveis globais:

- `SRC_FOLDER`: pasta com os arquivos python que deseja gerar os arquivos `.md`
- `SAVE_FOLDER`: pasta destino onde será salvo os arquivos `.md` de cada arquivo python
- `DEFAULT_INDENTATION`: número padrão de espaços utilizados na indentação dos arquivos `.py`

Após alterar as variáveis, execute o arquivo com o comando `python3 generate.py`.

### How it works

O script generate vai fazer o markdown de todos os arquivos dentro da pasta e sub pastas e gerará os arquivos `.md` com a mesma estrutura de diretório.

Ex:

Considere estrutura de diretório:
```
- core
   - arquivo.py
   - testes
        - test1.py
```

A saída será:

```       
- core
   - arquivo.md
   - testes
        - test1.md
```