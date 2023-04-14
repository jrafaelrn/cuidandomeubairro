# Ferramentas
---

Códigos auxiliares para o desenvolvimento do projeto.

### **Pesquisa de termos**
  
É necessário configurar 2 variáveis dentro do arquivo `find_terms.py`:
- TERMS_FILE = aponta para um arquivo TXT contendo uma lista de expressões regulares, uma por linha, que serão utilizadas para a pesquisa.
- FOLDER_PATH = aponta para a pasta onde estão os arquivos CSV que serão pesquisados *(extraídos no formato do TCESP-2022 inicialmente, outros poderão ser adicionados)*

Resultado esperado: e em uma pasta contendogera um arquivo `statistic_terms.csv` com os termos e suas respectivas frequências, no seguinte esquema:

| cidade | termo | frequencia |
|--------|-------|------------|
| Adamantina | praça | 10 |
| Adamantina | ponte | 5 |
| Adamantina | quadra | 2 |


Para executar é necessário instalar algumas bibliotecas:

` pip install unicode `

Depis para rodar o script:

` python find_terms.py `


