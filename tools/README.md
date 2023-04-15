# Ferramentas
---

Códigos auxiliares para o desenvolvimento do projeto.

### **Pesquisa de termos**
  
É necessário configurar 2 variáveis dentro do arquivo `search_terms.py`:
- TERMS_FILE = aponta para um arquivo TXT contendo uma lista de expressões regulares, uma por linha, que serão utilizadas para a pesquisa.
- FOLDER_PATH = aponta para a pasta onde estão os arquivos CSV que serão pesquisados *(extraídos no formato do TCESP-2022 inicialmente, outros poderão ser adicionados)*

O resultado esperado é a geração de 2 arquivos:
1. `statistic_terms.csv` com os termos e suas respectivas frequências. <br>
Os valores são  delimitados por `';'` pois os termos pesquisados são baseados em Regex, que pode conter `','` (informar a quantidade de ocorrências, por exemplo, `{3.5}`), o que poderia causar problemas ao fazer o parse do arquivo.<br>
O arquivo é gerado com o seguinte esquema:

| cidade | termo | frequencia | 
|--------|-------|------------| 
| Adamantina | praça | 10 |
| Adamantina | ponte | 5 |
| Adamantina | quadra | 2 |
| ... | ... | ... |
| total_rows |  | 100 |
<br>
2. `statistic_terms.json` com os termos e suas respectivas frequências, no seguinte esquema:

```json
{
    "Adamantina": {
        "av|avenida": 1,
        "praca": 5,
        "total_rows": 10
    },
    "Araçatuba": {
        "av|avenida": 10,
        "praca": 2,
        "total_rows": 12
    },
    ...
}
```

Para executar é necessário instalar algumas bibliotecas:

```bash
pip install unicode
```

Depis para rodar:

```bash
python search_terms.py
```


