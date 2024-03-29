# Ferramentas
---

Códigos auxiliares para o desenvolvimento do projeto.

### **Pesquisa de termos**
  
O resultado esperado é a geração de 2 arquivos:
1. `statistic_terms.csv` com os termos e suas respectivas frequências. <br>
Os valores são  delimitados por `';'` pois os termos pesquisados são baseados em Regex, que pode conter `','` (informar a quantidade de ocorrências, por exemplo, `{3.5}`), o que poderia causar problemas ao fazer o parse do arquivo.<br>
O arquivo é gerado com o seguinte esquema:

| cod_cidade    | cidade        | termo     | frequencia    | 
| ------------- | ------------- | --------- | ------------- |
| 12345         | Adamantina    | praça     | 10            |
| 12345         | Adamantina    | ponte     | 5             |
| 12345         | Adamantina    | quadra    | 2             |
| 12345         | ...           | ...       | ...           |
| 12345         | total_rows    |           | 100           |
| 12346         | Araçatuba     | praça     | 2             |
| 12346         | Araçatuba     | ponte     | 1             |
| 12346         | Araçatuba     | quadra    | 1             |
| 12346         | ...           | ...       | ...           |
| 12346         | total_rows    |           | 125           |
<br>

1. `statistic_terms.json` com os termos e suas respectivas frequências, no seguinte esquema:

```json
{
    "Adamantina": {
        "av|avenida": 1,
        "praca": 5,
        "total_rows": 10,
        "cod_cidade": 12345,
    },
    "Araçatuba": {
        "av|avenida": 10,
        "praca": 2,
        "total_rows": 12,
        "cod_cidade": 12346,
    },
    ...
}
```

Para executar é necessário instalar algumas bibliotecas:

```bash
pip install -r requirements.txt
```

Depis para rodar:

```bash
python run_elt_cmb.py
```


